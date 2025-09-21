from rest_framework.routers import DefaultRouter
from .views import *

#app name = 'TaiKhoan'

router = DefaultRouter()
router.register(r'quyen',QuyenV)
router.register(r'nhanvien',NhanVienV)
router.register(r'khachhang',KhachHangV)
router.register(r'',TaiKhoanV,basename='taikhoan')

urlpatterns = router.urls
