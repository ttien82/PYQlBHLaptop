from django.http import JsonResponse

def DangNhap_view(request):
    return JsonResponse({"hoadon": "test"})