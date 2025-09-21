from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

import TaiKhoan


# model cho bảng Quyền
class Quyen(models.Model):
    MaQuyen = models.CharField(max_length=20, primary_key=True)
    TenQuyen = models.CharField(max_length=50)

    def __str__(self):
        """"Trả về tên Quyền"""
        return self.TenQuyen

# dùng meta để django đọc model Quyền
    class Meta:
        managed = False
        db_table = 'Quyen'
        verbose_name='Quyền'
        verbose_name_plural='Quyền'


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
        managed = False
        db_table = 'NhanVien'
        verbose_name='Nhân viên'
        verbose_name_plural='Danh sách nhân viên'

    # model cho bảng Khách hàng
class KhachHang(models.Model):
    MaKH = models.CharField(max_length=20, primary_key=True)
    TenKH = models.CharField(max_length=255)
    DienThoai = models.CharField(max_length=15, null=True, blank=True)
    Email = models.CharField(max_length=255, null=True, blank=True)
    DiaChi = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        """"Trả về tên khách hàng"""
        return self.TenKH

# dùng meta để django đọc model khách hàng
    class Meta:
        managed = False
        db_table = 'KhachHang'
        verbose_name='Khách hàng'
        verbose_name_plural='Danh sách khách hàng'

class TaiKhoanManager(BaseUserManager):
    def create_user(self, TenDangNhap, password=None, **extra_fields):
        """Tạo tài khoản thường"""
        if not TenDangNhap:
            raise ValueError('Tên đăng nhập không được để trống')
        user = self.model(TenDangNhap=TenDangNhap, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, TenDangNhap, password=None,**extra_fields):
        """Tạo tài khoản admin"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        ma_quyen = extra_fields.pop('MaQuyen', None)
        if ma_quyen:
            try:
                quyen_instance = Quyen.objects.get(MaQuyen=ma_quyen)
                extra_fields['MaQuyen'] = quyen_instance
            except Quyen.DoesNotExist:
                raise ValueError(f"Không có mã quyền '{ma_quyen}'")

        return self.create_user(TenDangNhap, password, **extra_fields)

    # model cho bảng tài khoản kế thừa AbctractUser của Django
class TaiKhoan(AbstractBaseUser, PermissionsMixin ):
    id = models.AutoField(primary_key=True)
    MaTK = models.CharField(max_length=20, unique=True)
    TenDangNhap = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    # nếu MaNV bị xóa thì MaNV = null
    MaNV = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True, db_column='MaNV')
    MaKH = models.ForeignKey(KhachHang, on_delete=models.SET_NULL, null=True, blank=True,db_column='MaKH')
    MaQuyen = models.ForeignKey(Quyen, on_delete=models.SET_NULL, null=True, blank=True,db_column='MaQuyen')

    # Tắt Many to Many của  PermissionsMixin
    groups = None
    user_permissions = None

    #Django auth
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'TenDangNhap'
    REQUIRED_FIELDS = ['MaTK', 'MaQuyen']

    def has_perms(self, perm, obj = None):
        if self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return False

    objects = TaiKhoanManager()

    def __str__(self):
        return self.TenDangNhap

    class Meta:
        managed = False
        db_table = 'TaiKhoan'
        verbose_name  = "Tài khoản"
        verbose_name_plural = "Danh sách tài khoản"
        # ràng buộc dữ liệu MaNV và MaKH
        constraints = [
            models.CheckConstraint(
                check=models.Q(MaNV__isnull=True, MaKH__isnull=False) |
                      models.Q(MaNV__isnull=False, MaKH__isnull=True),
                name = 'CK_TaiKhoan_MaNV_MaKH'
            )
        ]