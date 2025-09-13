from django.http import JsonResponse

def SanPham_view(request):
    return JsonResponse({"hoadon": "test"})