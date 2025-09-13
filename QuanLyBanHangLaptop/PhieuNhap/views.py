from django.http import JsonResponse

def PhieuNhap_view(request):
    return JsonResponse({"hoadon": "test"})