from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PhieuNhap, ChiTietPhieuNhap
from .serializers import PhieuNhapSerializer, ChiTietPhieuNhapSerializer

def PhieuNhap_view(request):
    return JsonResponse({"PhieuNhap": "test"})


class PhieuNhapViewSet(viewsets.ModelViewSet):
    queryset = PhieuNhap.objects.all()
    serializer_class = PhieuNhapSerializer

class ChiTietPhieuNhapViewSet(viewsets.ModelViewSet):
    queryset = ChiTietPhieuNhap.objects.all()
    serializer_class = ChiTietPhieuNhapSerializer

    # Lấy chi tiết phiếu nhập theo MaPN
    @action(detail=False, methods=['get'], url_path='get-by-mapn/(?P<mapn>[^/.]+)')
    def get_by_mapn(self, request, mapn=None):
        chitiet = ChiTietPhieuNhap.objects.filter(MaPN=mapn)
        if not chitiet.exists():
            return Response({"detail": "Không tìm thấy dữ liệu"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(chitiet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Cập nhật chi tiết theo MaPN
    @action(detail=False, methods=['get','put'], url_path='update/(?P<mapn>[^/.]+)/(?P<masp>[^/.]+)')
    def update_by_mapn_masp(self, request, mapn=None, masp=None):
        try:
            chitiet = ChiTietPhieuNhap.objects.get(MaPN=mapn, MaSP=masp)
        except ChiTietPhieuNhap.DoesNotExist:
            return Response({'error': 'Không tìm thấy phiếu nhập'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(chitiet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa toàn bộ chi tiết theo mapn
    @action(detail=False, methods=['get','delete'], url_path='delete/(?P<mapn>[^/.]+)')
    def delete_by_mapn(self, request, mapn=None):
        chitiet = ChiTietPhieuNhap.objects.filter(MaPN=mapn)
        if not chitiet.exists():
            return Response({"detail": "Không tìm thấy chi tiết cho MaDH này"}, status=status.HTTP_404_NOT_FOUND)
        count = chitiet.count()
        chitiet.delete()
        return Response({"detail": f"Đã xóa {count} chi tiết của MaDH {mapn}"}, status=status.HTTP_204_NO_CONTENT)


    # Xóa chi tiết theo MaPN + MaSP
    @action(detail=False, methods=['get','delete'], url_path='delete/(?P<mapn>[^/.]+)/(?P<masp>[^/.]+)')
    def delete_by_mapn_masp(self, request, mapn=None, masp=None):
        chitiet = ChiTietPhieuNhap.objects.get(MaPN=mapn, MaSP=masp)
        if chitiet.exists():
            chitiet.delete()
            return Response({'message': 'Đã xóa thành công'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Không tìm thấy phiếu nhập'}, status=status.HTTP_404_NOT_FOUND)