from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonHangViewSet, ChiTietDonHangViewSet

router = DefaultRouter()
router.register(r'donhang', DonHangViewSet)
router.register(r'chitietdonhang', ChiTietDonHangViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
