from django.contrib import admin
from TaiKhoan.models import TaiKhoan, KhachHang, Quyen, NhanVien
from SanPham.models import NhaCungCap, LoaiSP, SanPham
from HoaDon.models import DonHang, ChiTietDonHang
from PhieuNhap.models import PhieuNhap, ChiTietPhieuNhap


admin.site.register(TaiKhoan)
admin.site.register(KhachHang)
admin.site.register(NhanVien)
admin.site.register(Quyen)
admin.site.register(SanPham)
admin.site.register(LoaiSP)
admin.site.register(NhaCungCap)
admin.site.register(ChiTietDonHang)
admin.site.register(DonHang)
admin.site.register(ChiTietPhieuNhap)
admin.site.register(PhieuNhap)