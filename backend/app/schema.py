from datetime import date
from ninja import Schema
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