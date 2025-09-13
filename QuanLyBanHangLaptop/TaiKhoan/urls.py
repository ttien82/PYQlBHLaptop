from django.urls import path
from . import views

urlpatterns = [
    path('', views.DangNhap_view),
]