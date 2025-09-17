from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

#app name = 'TaiKhoan'

router = DefaultRouter()
router.register(r'Quyền',QuyenV)
router.register(r'nhanvien',NhanVienV)
router.register(r'khachhang',KhachHangV)
router.register(r'taikhoan',TaiKhoanV)

urlpatterns = router.urls