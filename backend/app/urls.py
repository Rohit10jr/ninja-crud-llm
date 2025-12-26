from django.urls import path
from .views import api, home, text_view, AiView, CrudAiView

urlpatterns = [
    path('home/', home, name='home'),
    path("", api.urls), 
    path('text/', text_view, name='text_view'),
    path('text-api/', text_view, name='text_view'),
    path('ai-rsp/', AiView.as_view(), name='text_view'),
    path('ai-car/', CrudAiView.as_view(), name='text_view'),
]
