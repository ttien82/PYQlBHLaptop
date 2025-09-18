from django.db import models
from SanPham.models import SanPham

class DonHang(models.Model):
    MaDH = models.CharField(max_length=20, primary_key=True)
    MaKH = models.CharField(max_length=20, null=True, blank=True)
    MaNV = models.CharField(max_length=20)
    NgayLap = models.DateTimeField(auto_now_add=True)
    TongTien = models.DecimalField(max_digits=18, decimal_places=2)
    TrangThai = models.CharField(max_length=50)

    class Meta:
        db_table = 'DonHang'


class ChiTietDonHang(models.Model):
    id = models.AutoField(primary_key=True)
    MaDH = models.ForeignKey(
        DonHang,
        on_delete=models.CASCADE,
        db_column='MaDH'
    )
    MaSP = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        db_column='MaSP'
    )
    SoLuong = models.IntegerField()
    DonGia = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        unique_together = ('MaDH', 'MaSP')
        db_table = 'ChiTietDonHang'