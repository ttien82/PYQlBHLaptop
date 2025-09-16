from django.urls import path
from . import views

urlpatterns = [
# Sản phẩm
    path('', views.danh_sach_san_pham, name='danh_sach_san_pham'),
    path('them/', views.them_san_pham, name='add_san_pham'),
    path('sua/<str:ma_sp>/', views.sua_san_pham, name='sua_san_pham'),

# Loại sản phẩm
    path('loaisp/', views.danh_sach_loai_sp, name='danh_sach_loai_sp'),
    path('loaisp/them/', views.them_loai_sp, name='them_loai_sp'),
    path('loaisp/sua/<str:pk>/', views.sua_loai_sp, name='sua_loai_sp'),

# Nhà cung cấp
    path('ncc/', views.danh_sach_ncc, name='danh_sach_ncc'),
    path('ncc/them/', views.them_ncc, name='them_ncc'),
    path('ncc/sua/<str:pk>/', views.sua_ncc, name='sua_ncc'),
]
