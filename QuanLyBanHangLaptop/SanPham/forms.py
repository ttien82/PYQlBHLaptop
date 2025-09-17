from django import forms
from .models import SanPham, LoaiSP, NhaCungCap

class SanPhamForm(forms.ModelForm):
    class Meta:
        model = SanPham
        fields = ['MaSP', 'TenSP', 'MaLoaiSP', 'MaNCC', 'GiaBan', 'SoLuongTon','OCung','RAM','CardManHinh','HinhAnh','CPU']
        widgets = {
            'MaSP': forms.TextInput(attrs={'class': 'form-control '}),
            'TenSP': forms.TextInput(attrs={'class': 'form-control'}),
            'MaLoaiSP': forms.Select(attrs={'class': 'form-select'}),
            'MaNCC': forms.Select(attrs={'class': 'form-select'}),
            'GiaBan': forms.NumberInput(attrs={'class': 'form-control'}),
            'SoLuongTon': forms.NumberInput(attrs={'class': 'form-control '}),
            'OCung': forms.TextInput(attrs={'class': 'form-control'}),
            'CPU': forms.TextInput(attrs={'class': 'form-control'}),
            'RAM': forms.TextInput(attrs={'class': 'form-control'}),
            'CardManHinh': forms.TextInput(attrs={'class': 'form-control'}),
            'HinhAnh': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }
class LoaiSpForm(forms.ModelForm):
    class Meta:
        model = LoaiSP
        fields = ['MaLoaiSP', 'TenLoaiSP']
        widgets = {
            'MaLoaiSP': forms.TextInput(attrs={'class': 'form-control '}),
            'TenLoaiSP': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NhaCungCapForm(forms.ModelForm):
    class Meta:
        model = NhaCungCap
        fields = ['MaNCC', 'TenNCC','DiaChi','DienThoai']
        widgets = {
            'MaNCC': forms.TextInput(attrs={'class': 'form-control '}),
            'TenNCC': forms.TextInput(attrs={'class': 'form-control'}),
            'DiaChi': forms.TextInput(attrs={'class': 'form-control '}),
            'DienThoai': forms.TextInput(attrs={'class': 'form-control'}),
        }

