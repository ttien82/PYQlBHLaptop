from rest_framework import serializers
from SanPham.models import PhieuNhap, ChiTietPhieuNhap


#Dùng ModelSerializer để tự động map model -> JSON
class ChiTietPhieuNhapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiTietPhieuNhap
        fields = '__all__'


class PhieuNhapSerializer(serializers.ModelSerializer):
    chi_tiet = ChiTietPhieuNhapSerializer(many=True, read_only=True)

    class Meta:
        model = PhieuNhap
        fields = '__all__'
