from django.db import models
from SanPham.models import SanPham, NhaCungCap, NhanVien
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class PhieuNhap(models.Model):
    MaPN = models.CharField(max_length=20, primary_key=True)
    MaNCC = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE, db_column="MaNCC")
    MaNV = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column="MaNV")
    NgayNhap = models.DateTimeField(auto_now_add=True)
    TongTien = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = "PhieuNhap"
        verbose_name='Phiếu Nhập'
        verbose_name_plural='Phiếu Nhập'

    def __str__(self):
        return f"Phiếu nhập {self.MaPN}"


class ChiTietPhieuNhap(models.Model):
    MaCTPN = models.AutoField(primary_key=True, db_column='MaCTPN')
    MaPN = models.ForeignKey(
        'PhieuNhap',
        on_delete=models.CASCADE,
        db_column='MaPN'
    )
    MaSP = models.ForeignKey(
        'SanPham.SanPham',
        on_delete=models.CASCADE,
        db_column='MaSP'
    )
    SoLuong = models.PositiveIntegerField()
    GiaNhap = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = "ChiTietPhieuNhap"
        verbose_name='Chi Tiết Phiếu Nhập'
        verbose_name_plural='Chi Tiết Phiếu Nhập'
        unique_together = (("MaPN", "MaSP"),)


# ===== SIGNALS ĐỂ UPDATE TỔNG TIỀN =====
@receiver([post_save, post_delete], sender=ChiTietPhieuNhap)
def update_tong_tien(sender, instance, **kwargs):
    tong = ChiTietPhieuNhap.objects.filter(MaPN=instance.MaPN) \
               .aggregate(tong=Sum(models.F('SoLuong') * models.F('GiaNhap')))['tong'] or 0
    PhieuNhap.objects.filter(pk=instance.MaPN.pk).update(TongTien=tong)

def __str__(self):
    return f"{self.PhieuNhap.MaPN} - {self.SanPham.TenSP}"
