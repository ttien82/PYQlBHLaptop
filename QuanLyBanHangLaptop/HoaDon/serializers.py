from rest_framework import serializers
from .models import DonHang, ChiTietDonHang


#Dùng ModelSerializer để tự động map model -> JSON
class ChiTietDonHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDonHang
        fields = '__all__'


class DonHangSerializer(serializers.ModelSerializer):
    chi_tiet = ChiTietDonHangSerializer(many=True, read_only=True)

    class Meta:
        model = DonHang
        fields = '__all__'
