from django.http import JsonResponse


def HoaDon_view(request):
    return JsonResponse({"hoadon": "test"})


