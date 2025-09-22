from rest_framework import serializers , viewsets, status, filters
from rest_framework.response import Response
from .models import TaiKhoan, KhachHang, Quyen, NhanVien
from QuanLyBanHangLaptop.Ho_Tro import check_Quyen, TimKiem, TimKiem_tk, VietNamese

# Sử dụng serializers để chuyển đổi giữa model và Json
class QuyenS(VietNamese, serializers.ModelSerializer):
    class Meta:
        model = Quyen
        fields = '__all__'

    # dùng Tiếng Việt cho các định dạng
    vi = {
        "MaQuyen": "Mã quyền",
        "TenQuyen": "Tên quyền"
    }

class NhanVienS(VietNamese, serializers.ModelSerializer):
    class Meta:
        model = NhanVien
        fields = '__all__'

    vi = {
        "MaNV": "Mã nhân viên",
        "TenNV": "Tên nhân viên",
        "DiaChi": "Địa chỉ nhân viên",
        "DienThoai": "Điện thoại nhân viên"
    }

class KhachHangS(VietNamese, serializers.ModelSerializer):
    class Meta :
        model = KhachHang
        fields = '__all__'

    vi = {
        "MaKH": "Mã khách hàng",
        "TenKH": "Tên khách hàng",
        "DienThoai": "Điện thoại",
        "Email": "Email",
        "DiaChi": "Địa chỉ"
    }

class TaiKhoanS(VietNamese,serializers.ModelSerializer):
    MaQuyen = QuyenS(read_only=True)
    MaNV = NhanVienS(read_only=True)
    MaKH = KhachHangS(read_only=True)
    class Meta:
        model = TaiKhoan
        fields = ['MaTK', 'TenDangNhap', 'MaNV', 'MaKH', 'MaQuyen']

    vi = {
        "MaTK": "Mã tài khoản",
        "MaNV": "Mã nhân viên",
        "MaKH" : "Mã khách hàng",
        "TenDangNhap": "Tên đăng nhập",
        "MatKhau": "Mật khẩu",
        "MaQuyen": "Mã quyền"
    }


class QuyenV(TimKiem,viewsets.ModelViewSet):
    queryset = Quyen.objects.all()
    serializer_class = QuyenS
    lookup_field = 'MaQuyen'
    search_fields = ['MaQuyen', 'TenQuyen']

    # đổi tên tiêu đề
    def get_view_name(self):
        return "Danh sách quyền"

    # Phân quyền cho từng thao tác
    def list(self, request, *args, **kwargs):
        """"không có Quyền Admin lỗi trang"""
        if not check_Quyen(request.user, ['ADMIN']):
            return Response({'Giới hạn quyền truy cập'},status=status.HTTP_403_FORBIDDEN)
        return super(QuyenV, self).list(request, *args, **kwargs)

    """Admin đc truy cập"""
class NhanVienV(TimKiem, viewsets.ModelViewSet):
    queryset = NhanVien.objects.all()
    serializer_class = NhanVienS
    lookup_field = 'MaNV'
    search_fields = ['MaNV', 'TenNV','DiaChi','DienThoai']

    def get_view_name(self):
        return "Danh sách nhân viên"

    def list(self, request, *args, **kwargs):
        """"không có Quyền Admin lỗi trang"""
        if not check_Quyen(request.user, ['ADMIN']):
            return Response({'Giới hạn quyền truy cập'},status=status.HTTP_403_FORBIDDEN)
        return super(NhanVienV, self).list(request, *args, **kwargs)

    """Admin và Saff đc truy cập"""
class KhachHangV(TimKiem, viewsets.ModelViewSet):
    queryset = KhachHang.objects.all()
    serializer_class = KhachHangS
    lookup_field = 'MaKH'
    search_fields = ['MaKH', 'TenKH', 'Email', 'DienThoai', 'DiaChi']

    def get_view_name(self):
        return "Danh sách Khách hàng"

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

    """Chỉ admin mới có thể xóa"""
    def destroy(self, request, *args, **kwargs):
        if not check_Quyen(request.user, ['ADMIN']):
            return Response({'Không có quyền thao tác '},status=status.HTTP_403_FORBIDDEN)
        return super(KhachHangV, self).destroy(request, args, kwargs)

    """Admin đc truy cập"""
class TaiKhoanV(TimKiem_tk, viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all()
    serializer_class = TaiKhoanS
    lookup_field = 'MaTK'
    search_fields = ['MaQuyen__TenQuyen','TenDangNhap','MaTK']
    #permission_classes = [Admin]
    def get_view_name(self):
        return "Danh sách tài khoản"

    def get_queryset(self):
        user = self.request.user

        """"admin được xem toàn bộ, nv kh chỉ có thể xem tk của mình"""
        if check_Quyen(user, ['ADMIN']):
            # thêm điều kiện để tìm kiếm k xung đôt với phân quyền
            tk = TaiKhoan.objects.all()
        else:
            tk = TaiKhoan.objects.filter(TenDangNhap=user.TenDangNhap)
        return self.tim_kiem_tk(tk)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
