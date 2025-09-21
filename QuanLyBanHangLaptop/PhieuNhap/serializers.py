from rest_framework import serializers
from .models import PhieuNhap, ChiTietPhieuNhap
from QuanLyBanHangLaptop.Ho_Tro import VietNamese

#Dùng ModelSerializer để tự động map model -> JSON
class ChiTietPhieuNhapSerializer(VietNamese,serializers.ModelSerializer):
    class Meta:
        model = ChiTietPhieuNhap
        fields = '__all__'
    vi = {
        "MaCTPN": "Mã CTPN",
        "MaPN": "Mã Phiếu Nhập",
        "MaSP": "Mã Sản Phẩm",
        "SoLuong": "Số Lượng",
        "GiaNhap": "Giá Nhập"
    }

class PhieuNhapSerializer(VietNamese, serializers.ModelSerializer):
    chi_tiet = ChiTietPhieuNhapSerializer(many=True, read_only=True)

    class Meta:
        model = PhieuNhap
        fields = '__all__'
    vi = {
        "MaPN": "Mã Phiếu Nhập",
        "MaNCC": "Mã NCC",
        "MaNV": "Mã Nhân Viên",
        "NgayNhap": "Ngày Nhập",
        "TongTien": "Tổng Tiền"
    }
