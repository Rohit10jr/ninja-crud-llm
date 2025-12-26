from django.contrib import admin
from .models import Employee, Department, Car


admin.site.register(Car)
admin.site.register(Employee)
admin.site.register(Department)