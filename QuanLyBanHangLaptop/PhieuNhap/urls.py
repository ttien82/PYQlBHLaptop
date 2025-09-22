from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhieuNhapViewSet, ChiTietPhieuNhapViewSet

router = DefaultRouter()
router.register(r'', PhieuNhapViewSet,basename='phieunhap')
router.register(r'chitietphieunhap', ChiTietPhieuNhapViewSet,basename='ctphieunhap')

urlpatterns = [
    path('', include(router.urls)),
]
