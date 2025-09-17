
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import SanPham, LoaiSP, NhaCungCap
from django.http import HttpResponse, JsonResponse
import json

# Hiển thị danh sách sản phẩm
def danh_sach_san_pham(request):
    #1. Vào models lấy data
    sanphams = SanPham.objects.all().values().order_by('MaSP')
    #2. Trả về Json
    return JsonResponse(list(sanphams), safe=False)
# Thêm sản phẩm
@csrf_exempt  # Bỏ kiểm tra CSRF khi gửi từ Postman
def them_san_pham(request):
    #1. Kiểm tra xem có phải phương thức POST không
    if request.method == "POST":
        try:
            # 1. Lấy dữ liệu từ Json
            data = json.loads(request.body)
            MaSP = data.get("MaSP")
            TenSP = data.get("TenSP")
            MaNCC_id = data.get("MaNCC_id")
            MaLoaiSP_id = data.get("MaLoaiSP_id")
            CPU = data.get("CPU")
            RAM = data.get("RAM")
            OCung = data.get("OCung")
            CardManHinh = data.get("CardManHinh")
            GiaBan = data.get("GiaBan")
            SoLuongTon = data.get("SoLuongTon")
            HinhAnh = data.get("HinhAnh")

            # 2. Kiểm tra trùng mã sản phẩm
            if SanPham.objects.filter(MaSP=MaSP).exists():
                return JsonResponse({"success": False, "error": "Mã sản phẩm đã tồn tại."}, status=400)
            # 3. Kiểm tra đối tượng khóa ngoại
            try:
                MaNCC = NhaCungCap.objects.get(pk=MaNCC_id)
            except NhaCungCap.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Không tìm thấy nhà cung cấp '{MaNCC_id}'."},status=400)

            try:
                MaLoaiSP = LoaiSP.objects.get(pk=MaLoaiSP_id)
            except LoaiSP.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Không tìm thấy loại sản phẩm '{MaLoaiSP_id}'."}, status=400)

            # 3. Tạo sản phẩm mới
            sp = SanPham.objects.create(
                MaSP=MaSP,
                TenSP=TenSP,
                MaNCC=MaNCC,
                MaLoaiSP=MaLoaiSP,
                CPU=CPU,
                RAM=RAM,
                OCung=OCung,
                CardManHinh=CardManHinh,
                GiaBan=GiaBan,
                SoLuongTon=SoLuongTon,
                HinhAnh=HinhAnh
            )
            #4. Trả về Json
            return JsonResponse({
                "success": True,
                "message": "Thêm sản phẩm thành công.",
                "san_pham": model_to_dict(sp)
            }, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        else :
            return JsonResponse({"success": False, "error": "Không phải phương thức POST "}, status=405)

# Sửa sản phẩm
@csrf_exempt # Bỏ kiểm tra CSRF khi gửi từ Postman
def sua_san_pham(request):
    #1. Kiểm tra phương thức
    if request.method == "PUT":
        try:
            #2. Lấy dữ liệu json sửa
            data = json.loads(request.body)
            MaSP = data.get("MaSP")
            #3. Kiểm tra xem mã sản phẩm có tồn tại không
            try:
                sp = SanPham.objects.get(MaSP=MaSP)
            except SanPham.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Sản phẩm '{MaSP}' không tồn tại."}, status=404)

            # 4. Cập nhật các trường (nếu có gửi lên)
            sp.TenSP = data.get("TenSP", sp.TenSP)
            sp.CPU = data.get("CPU", sp.CPU)
            sp.RAM = data.get("RAM", sp.RAM)
            sp.OCung = data.get("OCung", sp.OCung)
            sp.CardManHinh = data.get("CardManHinh", sp.CardManHinh)
            sp.GiaBan = data.get("GiaBan", sp.GiaBan)
            sp.SoLuongTon = data.get("SoLuongTon", sp.SoLuongTon)
            sp.HinhAnh = data.get("HinhAnh", sp.HinhAnh)

            # 5.Cập nhật khóa ngoại nếu sửa
            MaNCC_id = data.get("MaNCC_id")
            if MaNCC_id:
                try:
                    sp.MaNCC = NhaCungCap.objects.get(pk=MaNCC_id)
                except NhaCungCap.DoesNotExist:
                    return JsonResponse({"success": False, "error": f"Nhà cung cấp '{MaNCC_id}' không tồn tại."}, status=400)

            MaLoaiSP_id = data.get("MaLoaiSP_id")
            if MaLoaiSP_id:
                try:
                    sp.MaLoaiSP = LoaiSP.objects.get(pk=MaLoaiSP_id)
                except LoaiSP.DoesNotExist:
                    return JsonResponse({"success": False, "error": f"Loại sản phẩm '{MaLoaiSP_id}' không tồn tại."}, status=400)
            #6. Lưu lại
            sp.save()
            #7. Trả về json
            return JsonResponse({
                "success": True,
                "message": "Sửa sản phẩm thành công.",
                "san_pham": model_to_dict(sp)
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ. Dùng PUT."}, status=405)

# Xóa sản phẩm
@csrf_exempt #Bỏ kiểm tra CSRF khi gửi từ Postman
def xoa_san_pham(request):
    # 1. Kiểm tra phương thức
    if request.method == "DELETE":
        try:
            # 2. Lấy dữ liệu json xóa
            data = json.loads(request.body)
            MaSP = data.get("MaSP")
            # 3. Kiểm tra xem mã sản phẩm có tồn tại không
            try:
                sp = SanPham.objects.get(MaSP=MaSP)
            except SanPham.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Sản phẩm '{MaSP}' không tồn tại."}, status=404)
            # 4. Xóa sản phẩm
            sp.delete()
            #5. Trả về json
            return JsonResponse({
                "success": True,
                "message": f"Đã xoá sản phẩm '{MaSP}' thành công."
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ. Dùng DELETE."}, status=405)

# Hiển thị danh sách loại Sản phẩm
def danh_sach_loai_sp(request):
    #1. Vào models lấy data
    loaisp = LoaiSP.objects.all().values().order_by('MaLoaiSP')
    #2. Trả về Json
    return JsonResponse(list(loaisp), safe=False)
# Thêm loại sản phẩm
@csrf_exempt  # Bỏ kiểm tra CSRF khi gửi từ Postman
def them_loai_sp(request):
    #1. Kiểm tra xem có phải phương thức POST không
    if request.method == "POST":
        try:
            # 1. Lấy dữ liệu từ Json
            data = json.loads(request.body)
            MaLoaiSP = data.get("MaLoaiSP")
            TenLoaiSP = data.get("TenLoaiSP")

            # 2. Kiểm tra trùng mã
            if LoaiSP.objects.filter(MaLoaiSP=MaLoaiSP).exists():
                return JsonResponse({"success": False, "error": "Mã loại sản phẩm đã tồn tại."}, status=400)

            # 3. Tạo loại sản phẩm mới
            loai = LoaiSP.objects.create(
                MaLoaiSP=MaLoaiSP,
                TenLoaiSP=TenLoaiSP
            )
            #4. Trả về Json
            return JsonResponse({
                "success": True,
                "message": "Thêm loại sản phẩm thành công.",
                "san_pham": model_to_dict(loai)
            }, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    else :
        return JsonResponse({"success": False, "error": "Không phải phương thức POST "}, status=405)

# Sửa loại sản phẩm
@csrf_exempt # Bỏ kiểm tra CSRF khi gửi từ Postman
def sua_loai_sp(request):
    #1. Kiểm tra phương thức
    if request.method == "PUT":
        try:
            #2. Lấy dữ liệu json sửa
            data = json.loads(request.body)
            MaLoaiSP = data.get("MaLoaiSP")
            #3. Kiểm tra xem mã loại sản phẩm có tồn tại không
            try:
                loai = LoaiSP.objects.get(MaLoaiSP=MaLoaiSP)
            except LoaiSP.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Loại sản phẩm '{MaLoaiSP}' không tồn tại."}, status=404)

            # 4. Cập nhật các trường (nếu có gửi lên)
            loai.TenLoaiSP = data.get("TenLoaiSP", loai.TenLoaiSP)

            #5. Lưu lại
            loai.save()
            #6. Trả về json
            return JsonResponse({
                "success": True,
                "message": "Sửa sản phẩm thành công.",
                "san_pham": model_to_dict(loai)
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ. Dùng PUT."}, status=405)

# Xóa loại sản phẩm
@csrf_exempt #Bỏ kiểm tra CSRF khi gửi từ Postman
def xoa_loai_sp(request):
    # 1. Kiểm tra phương thức
    if request.method == "DELETE":
        try:
            # 2. Lấy dữ liệu json xóa
            data = json.loads(request.body)
            MaLoaiSP = data.get("MaLoaiSP")
            # 3. Kiểm tra xem mã loại sản phẩm có tồn tại không
            try:
                loai = LoaiSP.objects.get(MaLoaiSP=MaLoaiSP)
            except LoaiSP.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Loại sản phẩm '{MaLoaiSP}' không tồn tại."}, status=404)
            # 4. Xóa loại sản phẩm
            loai.delete()
            #5. Trả về json
            return JsonResponse({
                "success": True,
                "message": f"Đã xoá loại sản phẩm '{MaLoaiSP}' thành công."
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ. Dùng DELETE."}, status=405)

# Hiển thị danh sách nhà cung cấp
def danh_sach_ncc(request):
    #1. Vào models lấy data
    ncc = NhaCungCap.objects.all().values().order_by('MaNCC')
    #2. Trả về Json
    return JsonResponse(list(ncc), safe=False)
# Thêm nhà cung cấp
@csrf_exempt  # Bỏ kiểm tra CSRF khi gửi từ Postman
def them_ncc(request):
    #1. Kiểm tra xem có phải phương thức POST không
    if request.method == "POST":
        try:
            # 1. Lấy dữ liệu từ Json
            data = json.loads(request.body)
            MaNCC = data.get("MaNCC")
            TenNCC = data.get("TenNCC")
            DiaChi = data.get("DiaChi")
            DienThoai = data.get("DienThoai")

            # 2. Kiểm tra trùng nhà cung cấp
            if NhaCungCap.objects.filter(MaNCC=MaNCC).exists():
                return JsonResponse({"success": False, "error": "Mã nhà cung cấp đã tồn tại."}, status=400)

            # 3. Tạo nhà cung cấp mới
            ncc = NhaCungCap.objects.create(
                MaNCC=MaNCC,
                TenNCC=TenNCC,
                DiaChi=DiaChi,
                DienThoai=DienThoai
            )
            #4. Trả về Json
            return JsonResponse({
                "success": True,
                "message": "Thêm nhà cung cấp thành công.",
                "san_pham": model_to_dict(ncc)
            }, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    else :
        return JsonResponse({"success": False, "error": "Không phải phương thức POST "}, status=405)

# Sửa nhà cung cấp
@csrf_exempt # Bỏ kiểm tra CSRF khi gửi từ Postman
def sua_ncc(request):
    #1. Kiểm tra phương thức
    if request.method == "PUT":
        try:
            #2. Lấy dữ liệu json sửa
            data = json.loads(request.body)
            MaNCC = data.get("MaNCC")
            #3. Kiểm tra xem mã sản phẩm có tồn tại không
            try:
                ncc = NhaCungCap.objects.get(MaNCC=MaNCC)
            except NhaCungCap.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Nhà cung cấp '{MaNCC}' không tồn tại."}, status=404)

            # 4. Cập nhật các trường (nếu có gửi lên)
            ncc.TenNCC = data.get("TenNCC", ncc.TenNCC)
            ncc.DiaChi = data.get("DiaChi", ncc.DiaChi)
            ncc.DienThoai = data.get("DienThoai", ncc.DienThoai)

            #5. Lưu lại
            ncc.save()
            #6. Trả về json
            return JsonResponse({
                "success": True,
                "message": "Sửa sản phẩm thành công.",
                "san_pham": model_to_dict(ncc)
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ. Dùng PUT."}, status=405)

# Xóa nhà cung cấp
@csrf_exempt #Bỏ kiểm tra CSRF khi gửi từ Postman
def xoa_ncc(request):
    # 1. Kiểm tra phương thức
    if request.method == "DELETE":
        try:
            # 2. Lấy dữ liệu json xóa
            data = json.loads(request.body)
            MaNCC = data.get("MaNCC")
            # 3. Kiểm tra xem mã nhà cung cấp có tồn tại không
            try:
                ncc = NhaCungCap.objects.get(MaNCC=MaNCC)
            except NhaCungCap.DoesNotExist:
                return JsonResponse({"success": False, "error": f"Nhà cung cấp '{MaNCC}' không tồn tại."}, status=404)
            # 4. Xóa nhà cung cấp
            ncc.delete()
            #5. Trả về json
            return JsonResponse({
                "success": True,
                "message": f"Đã xoá nhà cung cấp '{MaNCC}' thành công."
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ. Dùng DELETE."}, status=405)
