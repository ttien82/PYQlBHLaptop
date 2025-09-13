from django.urls import path
from . import views

urlpatterns = [
    path('', views.HoaDon_view),
]
