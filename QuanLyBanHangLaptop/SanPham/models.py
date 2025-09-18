from django.db import models

# Bảng Loại Sản Phẩm
class LoaiSP(models.Model):
    MaLoaiSP = models.CharField(max_length=20, primary_key=True)
    TenLoaiSP = models.CharField(max_length=100)

    def __str__(self):
        return self.TenLoaiSP

    class Meta:
        db_table = "LoaiSP"
        verbose_name = 'Loại sản phẩm'
        verbose_name_plural = 'Loại sản phẩm'

    @classmethod
    def create(cls, ma_loai, ten_loai):
        return cls.objects.create(MaLoaiSP=ma_loai, TenLoaiSP=ten_loai)

# Bảng Nhà Cung Cấp
class NhaCungCap(models.Model):
    MaNCC = models.CharField(max_length=20, primary_key=True)
    TenNCC = models.CharField(max_length=255)
    DiaChi = models.CharField(max_length=255, null=True, blank=True)
    DienThoai = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.TenNCC

    class Meta:
        db_table = "NhaCungCap"
        verbose_name = 'Nhà cung cấp'
        verbose_name_plural = 'Nhà cung cấp'

    @classmethod
    def create(cls, ma_ncc, ten_ncc, dia_chi=None, dien_thoai=None):
        return cls.objects.create(
            MaNCC=ma_ncc,
            TenNCC=ten_ncc,
            DiaChi=dia_chi,
            DienThoai=dien_thoai,
        )

# Bảng Sản Phẩm
class SanPham(models.Model):
    MaSP = models.CharField(max_length=20, primary_key=True)
    TenSP = models.CharField(max_length=255)

    MaNCC = models.ForeignKey('NhaCungCap', on_delete=models.SET_NULL, null=True, db_column='MaNCC')
    MaLoaiSP = models.ForeignKey('LoaiSP', on_delete=models.SET_NULL, null=True, db_column='MaLoaiSP')

    CPU = models.CharField(max_length=100, null=True, blank=True)
    RAM = models.CharField(max_length=50, null=True, blank=True)
    OCung = models.CharField(max_length=50, null=True, blank=True)
    CardManHinh = models.CharField(max_length=100, null=True, blank=True)
    GiaNhap = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    Thue = models.IntegerField(null=True, blank=True)
    GiaBan = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    SoLuongTon = models.IntegerField(null=True, blank=True)
    HinhAnh = models.CharField(max_length=255, null=True, blank=True)
    LaiGop = models.DecimalField(max_digits=18, decimal_places=0, null=True, blank=True)
    
    def __str__(self):
        return self.TenSP

    class Meta:
        db_table = "SanPham"
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        

    @classmethod
    def create(cls, ma_sp, ten_sp, ncc, loai_sp, **kwargs):
        return cls.objects.create(
            MaSP=ma_sp,
            TenSP=ten_sp,
            NhaCungCap=ncc,
            LoaiSP=loai_sp,
            **kwargs
        )
    
   # model cho bảng Nhân Viên
class NhanVien(models.Model):
    MaNV = models.CharField(max_length=20, primary_key=True)
    TenNV = models.CharField(max_length=255)
    DiaChi = models.CharField(max_length=255, null=True, blank=True)
    DienThoai = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        """"Trả về tên Nhân viên"""
        return self.TenNV

# dùng meta để django đọc model Nhân Viên
    class Meta:
        db_table = 'NhanVien'
        verbose_name='Nhân viên'
        verbose_name_plural='Danh sách nhân viên'


class PhieuNhap(models.Model):
    MaPN = models.CharField(max_length=20, primary_key=True)
    MaNCC = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE, db_column="MaNCC")
    MaNV = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column="MaNV")
    NgayNhap = models.DateTimeField(auto_now_add=True)
    TongTien = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = "PhieuNhap"

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
        'SanPham',
        on_delete=models.CASCADE,
        db_column='MaSP'
    )
    SoLuong = models.PositiveIntegerField()
    GiaNhap = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = "ChiTietPhieuNhap"
        unique_together = (("MaPN", "MaSP"),)


    def __str__(self):
        return f"{self.PhieuNhap.MaPN} - {self.SanPham.TenSP}"
