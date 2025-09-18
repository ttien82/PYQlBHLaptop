from django.http import JsonResponse
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import *

# Sử dụng serializers để chuyển đổi giữa model và Json
class QuyenS(serializers.ModelSerializer):
    class Meta:
        model = Quyen
        fields = '__all__'

class NhanVienS(serializers.ModelSerializer):
    class Meta:
        model = NhanVien
        fields = '__all__'

class KhachHangS(serializers.ModelSerializer):
    class Meta :
        model = KhachHang
        fields = '__all__'

class TaiKhoanS(serializers.ModelSerializer):
    MaQuyen = QuyenS(read_only=True)
    MaNV = NhanVienS(read_only=True)
    MaKH = KhachHangS(read_only=True)
    class Meta:
        model = TaiKhoan
        fields = ['MaTK', 'TenDangNhap', 'MaNV', 'MaKH', 'MaQuyen']

# Kiểm tra Quyền
'''
class Admin(permissions.BasePermission):
    """Các trang chỉ Admin được truy cập"""
    def has_permission(self, request, view):
        # Kiểm tra có phải admin ko
        return (request.user.is_authenticated and
                (request.user.is_superuser or
                 (request.user.MaQuyen and
                request.user.MaQuyen.MaQuyen == 'ADMIN')))

class AdminOrStaff(permissions.BasePermission):
    """"Các trang admin và staff được truy cập"""
    def has_permission(self, request, view):
    # Kiểm tra có phải admin hoặc staff ko
        return (request.user.is_authenticated and
                (request.user.is_superuser or
                request.user.MaQuyen and
                (request.user.MaQuyen.MaQuyen == 'STAFF' or
                 request.user.MaQuyen.MaQuyen == 'ADMIN')))


class Customer(permissions.BasePermission):
    """Các trang customer truy cập"""
    def has_permission(self, request, view):
        #Kiểm tra có phải customer ko
        return (request.user.is_authenticated and
                (request.user.is_superuser or
                request.user.MaQuyen and
                request.user.MaQuyen.MaQuyen == 'CUSTOMER'))
'''

class SuperUser(permissions.BasePermission):
    """"Dành cho người có is_superuser=True"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.is_superuser)

# Hàm kiểm tra Quyền
def check_Quyen(user, vai_tro):
    return (
        user.is_authenticated and
        user.MaQuyen.MaQuyen and
        user.MaQuyen.MaQuyen in vai_tro
    )

# Phân Quyền cho từng trang
    """Admin đc truy cập"""
class QuyenV(viewsets.ModelViewSet):
    queryset = Quyen.objects.all()
    serializer_class = QuyenS

    def list(self, request, *args, **kwargs):
        """"không có Quyền Admin lỗi trang"""
        if not check_Quyen(request.user, ['ADMIN']):
            return Response({'Giới hạn quyền truy cập'},status=status.HTTP_403_FORBIDDEN)
        return super(QuyenV, self).list(request, *args, **kwargs)

    """Admin đc truy cập"""
class NhanVienV(viewsets.ModelViewSet):
    queryset = NhanVien.objects.all()
    serializer_class = NhanVienS
    #permission_classes = [Admin]

    def list(self, request, *args, **kwargs):
        """"không có Quyền Admin lỗi trang"""
        if not check_Quyen(request.user, ['ADMIN']):
            return Response({'Giới hạn quyền truy cập'},status=status.HTTP_403_FORBIDDEN)
        return super(NhanVienV, self).list(request, *args, **kwargs)

    """Admin và Saff đc truy cập"""
class KhachHangV(viewsets.ModelViewSet):
    queryset = KhachHang.objects.all()
    serializer_class = KhachHangS
    #permission_classes = [AdminOrStaff]

    def list(self, request, *args, **kwargs):
        """"không có Quyền Admin hoặc STAFF lỗi trang"""
        if not check_Quyen(request.user, ['ADMIN','STAFF']):
            return Response({'Giới hạn quyền truy cập'},status=status.HTTP_403_FORBIDDEN)
        return super(KhachHangV, self).list(request, *args, **kwargs)


    """Chỉ admin hoặc staff được phép thêm sửa"""
    def create(self, request, *args, **kwargs):
        if not check_Quyen(request.user, ['ADMIN','STAFF']):
            return Response({'Không có quyền thao tác '},status=status.HTTP_403_FORBIDDEN)
        return super(KhachHangV, self).create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        if not check_Quyen(request.user, ['ADMIN','STAFF']):
            return Response({'Không có quyền thao tác '},status=status.HTTP_403_FORBIDDEN)
        return super(KhachHangV, self).update(request, args, kwargs)

    """Chỉ admin mới có thể xóa sản phẩm"""
    def destroy(self, request, *args, **kwargs):
        if not check_Quyen(request.user, ['ADMIN']):
            return Response({'Không có quyền thao tác '},status=status.HTTP_403_FORBIDDEN)
        return super(KhachHangV, self).destroy(request, args, kwargs)

    """Admin đc truy cập"""
class TaiKhoanV(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all()
    serializer_class = TaiKhoanS
    #permission_classes = [Admin]

    def list(self, request, *args, **kwargs):
        """"không có Quyền Admin lỗi trang"""
        if not check_Quyen(request.user, ['ADMIN']):
            return Response({'Giới hạn quyền truy cập'},status=status.HTTP_403_FORBIDDEN)
        return super(TaiKhoanV, self).list(request, *args, **kwargs)

