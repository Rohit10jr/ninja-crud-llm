from typing import List

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from ninja import NinjaAPI, Schema 
from ninja import UploadedFile, File

from .schema import EmployeeIn, EmployeeOut
from .models import Employee


STORAGE = FileSystemStorage()

api = NinjaAPI()

def home(request):
    return HttpResponse("Hello, this is the home page.")

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