from . import views
from django.urls import path

urlpatterns = [
    path('', views.api_status, name='api_status'),
]
