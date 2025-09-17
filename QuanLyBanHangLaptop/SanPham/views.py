from django.shortcuts import render, redirect, get_object_or_404
from .models import SanPham, LoaiSP, NhaCungCap
from .forms import SanPhamForm, LoaiSpForm, NhaCungCapForm
from django.core.paginator import Paginator

# Hiển thị danh sách sản phẩm
def danh_sach_san_pham(request):
    sanphams = SanPham.objects.all().order_by('MaSP')
    paginator = Paginator(sanphams, 10)  # mỗi trang 10 sản phẩm
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sanpham/list.html', {
        'page_obj': page_obj
    })


# Thêm sản phẩm (trang riêng)
def them_san_pham(request):
    if request.method == "POST":
        form = SanPhamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("danh_sach_san_pham")
    else:
        form = SanPhamForm()

    return render(request, "sanpham/form.html", {
        "form": form,
        "title": "Thêm sản phẩm"
    })


# Sửa sản phẩm (trang riêng)
def sua_san_pham(request, ma_sp):
    sp = get_object_or_404(SanPham, pk=ma_sp)
    if request.method == "POST":
        form = SanPhamForm(request.POST, instance=sp)
        if form.is_valid():
            form.save()
            return redirect("danh_sach_san_pham")
    else:
        form = SanPhamForm(instance=sp)

    return render(request, "sanpham/form.html", {
        "form": form,
        "title": "Sửa sản phẩm"
    })
def danh_sach_loai_sp(request):
    ds_loai = LoaiSP.objects.all().order_by('MaLoaiSP')
    paginator = Paginator(ds_loai, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'sanpham/list_loaiSp.html', {'page_obj': page_obj})

### Loại Sản phẩm
def them_loai_sp(request):
    if request.method == 'POST':
        form = LoaiSpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_loai_sp')
    else:
        form = LoaiSpForm()
    return render(request, 'sanpham/form_loaiSp.html', {'form': form, 'title': 'Thêm loại sản phẩm'})

def sua_loai_sp(request, pk):
    loai = get_object_or_404(LoaiSP, pk=pk)
    if request.method == 'POST':
        form = LoaiSpForm(request.POST, instance=loai)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_loai_sp')
    else:
        form = LoaiSpForm(instance=loai)
    return render(request, 'sanpham/form_loaiSp.html', {'form': form, 'title': 'Sửa loại sản phẩm'})

#### NHÀ CUNG CẤP
def danh_sach_ncc(request):
    ncc = NhaCungCap.objects.all().order_by('MaNCC')
    paginator = Paginator(ncc, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'sanpham/list_ncc.html', {'page_obj': page_obj})

def them_ncc(request):
    if request.method == 'POST':
        form = NhaCungCapForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_ncc')
    else:
        form = NhaCungCapForm()
    return render(request, 'sanpham/form_ncc.html', {'form': form, 'title': 'Thêm nhà cung cấp'})

def sua_ncc(request, pk):
    ncc = get_object_or_404(NhaCungCap, pk=pk)
    if request.method == 'POST':
        form = NhaCungCapForm(request.POST, instance=ncc)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_ncc')
    else:
        form = NhaCungCapForm(instance=ncc)
    return render(request, 'sanpham/form_ncc.html', {'form': form, 'title': 'Sửa thông tin nhà cung cấp'})
