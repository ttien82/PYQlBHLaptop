from django.contrib import admin
from TaiKhoan.models import *
from SanPham.models import *
from HoaDon.models import *
from PhieuNhap.models import *


admin.site.register(TaiKhoan)
admin.site.register(KhachHang)
admin.site.register(NhanVien)
admin.site.register(Quyen)
admin.site.register(SanPham)
admin.site.register(LoaiSP)
admin.site.register(NhaCungCap)