from rest_framework import serializers
from .models import DonHang, ChiTietDonHang
from QuanLyBanHangLaptop.Ho_Tro import VietNamese

#Dùng ModelSerializer để tự động map model -> JSON
class ChiTietDonHangSerializer(VietNamese,serializers.ModelSerializer):
    class Meta:
        model = ChiTietDonHang
        fields = '__all__'

    vi = {
        "MaCTDH": "Mã chi tiết hóa đơn",
        "MaDH": "Mã hóa đơn",
        "MaSP": "Mã sản phẩm",
        "SoLuong": "Số lượng",
        "DonGia": "Đơn giá"
    }

class DonHangSerializer(VietNamese,serializers.ModelSerializer):
    chi_tiet = ChiTietDonHangSerializer(many=True, read_only=True)

    class Meta:
        model = DonHang
        fields = '__all__'

    vi = {
        "MaDH": "Mã hóa đơn",
        "MaKH": "Mã khách hàng",
        "MaNV": "Mã nhân viên",
        "NgayLap": "Ngày lập",
        "TongTien": "Tổng tiền",
        "TrangThai": "Trạng thái"
    }
