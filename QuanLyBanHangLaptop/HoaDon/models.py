from django.db import models
from SanPham.models import SanPham
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class DonHang(models.Model):
    MaDH = models.CharField(max_length=20, primary_key=True)
    MaKH = models.CharField(max_length=20, null=True, blank=True)
    MaNV = models.CharField(max_length=20)
    NgayLap = models.DateTimeField(auto_now_add=True)
    TongTien = models.DecimalField(max_digits=18, decimal_places=2)
    TrangThai = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'DonHang'
        verbose_name = 'Đơn Hàng'
        verbose_name_plural = 'Đơn Hàng'

class ChiTietDonHang(models.Model):
    MaCTDH = models.AutoField(primary_key=True)
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
        managed = False
        unique_together = ('MaDH', 'MaSP')
        verbose_name = 'Chi Tiết Đơn Hàng'
        verbose_name_plural = 'Chi Tiết Đơn Hàng'
        db_table = 'ChiTietDonHang'

# ===== SIGNALS ĐỂ UPDATE TỔNG TIỀN =====
@receiver([post_save, post_delete], sender=ChiTietDonHang)
def update_tong_tien(sender, instance, **kwargs):
    tong = ChiTietDonHang.objects.filter(MaDH=instance.MaDH) \
               .aggregate(tong=Sum(models.F('SoLuong') * models.F('DonGia')))['tong'] or 0
    DonHang.objects.filter(pk=instance.MaDH.pk).update(TongTien=tong)