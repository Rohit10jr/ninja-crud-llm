import json
from typing import List
from decimal import Decimal

from django.forms.models import model_to_dict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema, Router
from ninja import UploadedFile, File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
import os 
from dotenv import load_dotenv

from .serializer import TextSerializer 
from .schema import EmployeeIn, EmployeeOut, CarIn, CarOut, CarUpdate, CarCreateInput, CarUpdateInput, CarDeleteInput
from .models import Employee, Car
from google import genai

load_dotenv()

# STORAGE = FileSystemStorage()

api_key = os.getenv("GROK_API_KEY")

def home(request):
    return HttpResponse("Hello, this is the home page.")


@csrf_exempt
def text_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        serializer = TextSerializer(data=data)

        if serializer.is_valid():
            text = serializer.validated_data["text"]
            return JsonResponse({"message": f"You submitted: {text}"})

        return JsonResponse(serializer.errors, status=400)

    return HttpResponse("Hello, share some text!")


class TextView(APIView):
    def get(self, request):
        return HttpResponse("Hello, this is the Text return endpoint.")
    def post(self, request):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": f"You submitted: {serializer.validated_data['text']}"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


search = DuckDuckGoSearchRun()

model = ChatGroq(
    model = "qwen/qwen3-32b",
    temperature=0.1,
    max_tokens=1000,
    timeout=30,
    api_key=api_key
)

@tool
def web_search(query: str) -> str:
    """Perform a web search and return the results."""
    return search.invoke(query)

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(model, tools=[get_weather, web_search], system_prompt="You are a helpful assistant")


class AiView(APIView):
    def get(self, request):
        return HttpResponse("Hello, this is the AI response endpoint.")
    def post(self, request):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            user_query = serializer.validated_data.get('text')
            ai_state = agent.invoke(
                {"messages": [{"role": "user", "content": user_query}]}
            )
            f"You submitted: {serializer.validated_data['text']}"
            final_answer = ai_state["messages"][-1].content
            return Response(
                {"message": final_answer},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##################################################


car_model = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature=0.1,
    max_tokens=1000,
    timeout=30,
    api_key=api_key
)

@tool
def car_get_all() -> list[dict]:
    """
    Use this tool to fetch all car details from the database.
    Returns a list of cars with full attributes.
    """
    cars = Car.objects.all()
    return [model_to_dict(car) for car in cars]

@tool
def car_get_one(car_id: int) -> dict:
    """
    Use this tool to fetch a specific car by its ID.
    Input: car_id (integer)
    Returns full car details.
    """
    car = get_object_or_404(Car, id=car_id)
    return model_to_dict(car)

@tool(args_schema=CarCreateInput)
def car_post(
    manufacturer: str,
    model_name: str,
    year: int,
    color: str,
    price: float,
    is_used: bool = False,
) -> dict:
    """
    Create a new car entry in the database.
    Use this tool ONLY when the user wants to add a new car.
    """
    car = Car.objects.create(
        manufacturer=manufacturer,
        model_name=model_name,
        year=year,
        color=color,
        price=price,
        is_used=is_used,
    )
    return model_to_dict(car)

@tool(args_schema=CarUpdateInput)
def car_update(
    car_id: int,
    manufacturer: str | None = None,
    model_name: str | None = None,
    year: int | None = None,
    color: str | None = None,
    price: float | None = None,
    is_used: bool | None = None,
) -> dict:
    """
    Update an existing car.
    Use this tool when the user wants to modify car details.
    """
    car = get_object_or_404(Car, id=car_id)

    update_data = {
        "manufacturer": manufacturer,
        "model_name": model_name,
        "year": year,
        "color": color,
        "price": price,
        "is_used": is_used,
    }

    for field, value in update_data.items():
        if value is not None:
            setattr(car, field, value)

    car.save()
    return model_to_dict(car)

@tool(args_schema=CarDeleteInput)
def car_delete(car_id: int) -> dict:
    """
    Delete a car from the database.
    Use this tool ONLY when the user explicitly asks to remove a car.
    """
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return {"success": True, "deleted_car_id": car_id}

    
crud_agent = create_agent(car_model, tools=[car_get_all, car_get_one, car_post, car_update, car_delete, web_search], system_prompt="You are a helpful assistant that manages car records in a database and performs web search. Use the provided tools to perform CRUD operations on cars based on user requests.")


class CrudAiView(APIView):
    def get(self, request):
        return HttpResponse("Hello, this is the CAR AI CRUD endpoint.")
    def post(self, request):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            user_query = serializer.validated_data.get('text')
            ai_state = crud_agent.invoke(
                {"messages": [{"role": "user", "content": user_query}]}
            )
            f"You submitted: {serializer.validated_data['text']}"
            final_answer = ai_state["messages"][-1].content
            return Response(
                {"message": final_answer},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


api = NinjaAPI()
router = Router(tags=["Cars"])
api.add_router("", router)

# car crud operations
@router.post("/cars", response=CarOut)
def create_car(request, payload: CarIn):
    car = Car.objects.create(**payload.dict())
    return car

@router.get("/cars", response=list[CarOut])
def list_cars(request):
    return Car.objects.all()

@router.get("/cars/{car_id}", response=CarOut)
def get_car(request, car_id: int):
    return get_object_or_404(Car, id=car_id)

@router.put("/cars/{car_id}", response=CarOut)
def update_car(request, car_id: int, payload: CarIn):
    car = get_object_or_404(Car, id=car_id)

    for attr, value in payload.dict().items():
        setattr(car, attr, value)

    car.save()
    return car

@router.patch("/cars/{car_id}", response=CarOut)
def patch_car(request, car_id: int, payload: CarUpdate):
    car = get_object_or_404(Car, id=car_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(car, attr, value)

    car.save()
    return car

@router.delete("/cars/{car_id}")
def delete_car(request, car_id: int):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return {"success": True}


# Employee CRUD operations
# Create
@api.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


# Retrieve - Single object
@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


# Retrieve - List of objects
@api.get("/employees", response=List[EmployeeOut])
def list_employees(request):
    qs = Employee.objects.all()
    return qs


# Update
@api.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}

# Partial updates
# To allow the user to make partial updates, use payload.dict(exclude_unset=True).items()


# Delete
@api.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}