from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhieuNhapViewSet, ChiTietPhieuNhapViewSet

router = DefaultRouter()
router.register(r'phieunhap', PhieuNhapViewSet)
router.register(r'chitietphieunhap', ChiTietPhieuNhapViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
