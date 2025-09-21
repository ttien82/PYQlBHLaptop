from rest_framework import serializers
from .models import DonHang, ChiTietDonHang
from QuanLyBanHangLaptop.Ho_Tro import VietNamese

#Dùng ModelSerializer để tự động map model -> JSON
class ChiTietDonHangSerializer(VietNamese,serializers.ModelSerializer):
    class Meta:
        model = ChiTietDonHang
        fields = '__all__'
    vi = {
        "MaCTDH": "Mã CTDH",
        "SoLuong": "Số Lượng",
        "DonGia": "Đơn Giá",
        "MaDH": "Mã Đơn Hàng",
        "MaSP": "Mã SP"
    }

    vi = {
        "MaDH": "Mã đơn hàng",
        "MaKH": "Khách hàng",
        "NgayLap": "Ngày lập",
        "TongTien": "Tổng tiền",
        "TrangThai": "Trạng thái"
    }


class DonHangSerializer(VietNamese,serializers.ModelSerializer):
    chi_tiet = ChiTietDonHangSerializer(many=True, read_only=True)

    class Meta:
        model = DonHang
        fields = '__all__'
    vi = {
        "MaPN": "Mã Phiếu Nhập",
        "MaNCC": "Mã NCC",
        "MaNV": "Mã Nhân Viên",
        "NgayNhap": "Ngày Nhập",
        "TongTien": "Tổng Tiền"
    }
