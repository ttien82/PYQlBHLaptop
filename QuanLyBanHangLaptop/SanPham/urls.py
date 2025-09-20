from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
     path('', views.danh_sach_san_pham, name='danh_sach_san_pham'),
     path('them/', views.them_san_pham, name='them_san_pham'),
     path('sua/', views.sua_san_pham, name='sua_san_pham'),
     path('xoa/', views.xoa_san_pham, name='xoa_san_pham'),
     path('loaisp/', views.danh_sach_loai_sp, name='danh_sach_loai_sp'),
     path('loaisp/them/', views.them_loai_sp, name='them_loai_sp'),
     path('loaisp/sua/', views.sua_loai_sp, name='sua_loai_sp'),
     path('loaisp/xoa/', views.xoa_loai_sp, name='xoa_loai_sp'),
     path('ncc/', views.danh_sach_ncc, name='danh_sach_ncc'),
     path('ncc/them/', views.them_ncc, name='them_ncc'),
     path('ncc/sua/', views.sua_ncc, name='sua_ncc'),
     path('ncc/xoa/', views.xoa_ncc, name='xoa_ncc'),

]
router = DefaultRouter()
urlpatterns += router.urls
router.register(r'', views.SanPhamV,basename='sanpham')
router.register(r'', views.NhaCungCapV,basename='ncc')
router.register(r'',views.LoaiSPV,basename='loaisp')
