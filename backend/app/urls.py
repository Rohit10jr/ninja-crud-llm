from django.urls import path
from .views import home, api

urlpatterns = [
    path('home/', home, name='home'),
    path("", api.urls), 
]
