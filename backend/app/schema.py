from datetime import date
from ninja import Schema
from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Literal, Optional
from decimal import Decimal


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class CarIn(Schema):
    manufacturer: str
    model_name: str
    year: int
    color: str
    price: Decimal
    is_used: bool = True


class CarOut(Schema):
    id: int
    manufacturer: str
    model_name: str
    year: int
    color: str
    price: Decimal
    is_used: bool


class CarUpdate(Schema):
    manufacturer: str | None = None
    model_name: str | None = None
    year: int | None = None
    color: str | None = None
    price: Decimal | None = None
    is_used: bool | None = None


class CarCreateInput(BaseModel):
    """Input for car create operations."""
    manufacturer: str = Field(description="Car manufacturer")
    model_name: str = Field(description="Car model name")
    year: int = Field(description="Manufacturing year")
    color: str = Field(description="Car color")
    price: float  = Field(description="Car price")
    is_used: bool = Field(default=True, description="Whether the car is used")


class CarUpdateInput(BaseModel):
    """Input for car update operations."""
    car_id: int = Field(default=None, description="ID of the car to update")
    manufacturer: str = Field(default=None, description="Car manufacturer")
    model_name: str = Field(default=None, description="Car model name")
    year: int = Field(default=None, description="Manufacturing year")
    color: str = Field(default=None, description="Car color")
    price: float  = Field(default=None, description="Car price")
    is_used: bool = Field(default=True, description="Whether the car is used")


class CarDeleteInput(BaseModel):
    """Input for car delete operations."""
    car_id: int = Field(description="ID of the car to delete")