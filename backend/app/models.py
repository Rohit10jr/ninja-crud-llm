from django.db import models


class Department(models.Model):
    title = models.CharField(max_length=100)


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    cv = models.FileField(null=True, blank=True)
    

class Car(models.Model):
    manufacturer = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_used = models.BooleanField(default=True)

    def __str__(self):
        """String representation used in the admin interface"""
        status = "Used" if self.is_used else "New"
        return f"{self.manufacturer} {self.model_name} ({self.year}) - {status}"

    