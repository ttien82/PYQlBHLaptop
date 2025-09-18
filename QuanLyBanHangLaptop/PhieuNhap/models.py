from django.db import models
from SanPham.models import SanPham

class PhieuNhap(models.Model):
    MaPN = models.CharField(max_length=20, primary_key=True)
    MaNCC = models.CharField(max_length=20)
    MaNV = models.CharField(max_length=20)
    NgayNhap = models.DateTimeField(auto_now_add=True)
    TongTien = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'PhieuNhap'


class ChiTietPhieuNhap(models.Model):
    MaPN = models.ForeignKey(
        PhieuNhap,
        on_delete=models.CASCADE,
        db_column='MaPN'
    )
    MaSP = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        db_column='MaSP'
    )
    SoLuong = models.IntegerField()
    GiaNhap = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        unique_together = ('MaPN', 'MaSP')
        db_table = 'ChiTietPhieuNhap'
