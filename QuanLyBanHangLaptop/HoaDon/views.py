from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DonHang, ChiTietDonHang
from .serializers import DonHangSerializer, ChiTietDonHangSerializer
from django.db.models import Sum

class DonHangViewSet(viewsets.ModelViewSet):
    queryset = DonHang.objects.all()
    serializer_class = DonHangSerializer


class ChiTietDonHangViewSet(viewsets.ModelViewSet):
    queryset = ChiTietDonHang.objects.all()
    serializer_class = ChiTietDonHangSerializer

    # Lấy chi tiết theo MaDH
    @action(detail=False, methods=['get'], url_path='get-by-madh/(?P<madh>[^/.]+)')
    def get_by_madh(self, request, madh=None):
        chitiet = ChiTietDonHang.objects.filter(MaDH=madh)
        if not chitiet.exists():
            return Response({"detail": "Không tìm thấy dữ liệu"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(chitiet, many=True).data, status=status.HTTP_200_OK)

    # Cập nhật theo MaDH + MaSP
    @action(detail=False, methods=['get','put'], url_path='update/(?P<madh>[^/.]+)/(?P<masp>[^/.]+)')
    def update_by_madh_masp(self, request, madh=None, masp=None):
        try:
            chitiet = ChiTietDonHang.objects.get(MaDH=madh, MaSP=masp)
        except ChiTietDonHang.DoesNotExist:
            return Response({"detail": "Không tìm thấy dữ liệu"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(chitiet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa toàn bộ chi tiết theo madh
    @action(detail=False, methods=['get','delete'], url_path='delete/(?P<madh>[^/.]+)')
    def delete_by_madh(self, request, madh=None):
        chitiet = ChiTietDonHang.objects.filter(MaDH=madh)
        if not chitiet.exists():
            return Response({"detail": "Không tìm thấy chi tiết cho MaDH này"}, status=status.HTTP_404_NOT_FOUND)
        count = chitiet.count()
        chitiet.delete()
        return Response({"detail": f"Đã xóa {count} chi tiết của MaDH {madh}"}, status=status.HTTP_204_NO_CONTENT)

    # Xóa 1 chi tiết theo MaDH + MaSP
    @action(detail=False, methods=['get','delete'], url_path='delete/(?P<madh>[^/.]+)/(?P<masp>[^/.]+)')
    def delete_by_madh_masp(self, request, madh=None, masp=None):
        try:
            chitiet = ChiTietDonHang.objects.get(MaDH=madh, MaSP=masp)
        except ChiTietDonHang.DoesNotExist:
            return Response({"detail": "Không tìm thấy chi tiết này"}, status=status.HTTP_404_NOT_FOUND)
        chitiet.delete()
        return Response({"detail": f"Đã xóa chi tiết {masp} của MaDH {madh}"}, status=status.HTTP_204_NO_CONTENT)

    # 1. Top 10 Sản phẩm bán chạy nhất
    @action(detail=False, methods=['get'], url_path='san-pham-ban-chay')
    def san_pham_ban_chay(self, request):
        result = (ChiTietDonHang.objects
                  .values('MaSP')
                  .annotate(tong_so_luong=Sum('SoLuong'))
                  .order_by('-tong_so_luong')[:10])
        return Response(result)

    # 2. Top 20 Khách hàng mua nhiều nhất
    @action(detail=False, methods=['get'], url_path='khach-hang-mua-nhieu')
    def khach_hang_mua_nhieu(self, request):
        result = (DonHang.objects
                  .values('MaKH')
                  .annotate(tong_tien=Sum('TongTien'))
                  .order_by('-tong_tien')[:20])
        return Response(result)
