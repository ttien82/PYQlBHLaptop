from ..models import ChiTietPhieuNhap, PhieuNhap, SanPham
from django.db.models import OuterRef, Subquery


class GiaNhap:
    def __init__(self, Dot ):
        self.__Dot = Dot
        self.__ds_sp = []

    def init_ds_sp(self, list):
        self.__ds_sp = list

    @property
    def ds_sp(self):
        return self.__ds_sp

    def tinh(self):
        """Tính giá nhập cho các sản phẩm"""
        for sp in self.ds_sp:  # sp là dict
            ctpn = (
                ChiTietPhieuNhap.objects
                .filter(MaSP=sp["MaSP"])
                .select_related("MaPN")
                .order_by('-MaPN__NgayNhap')
                .first()
            )
            if ctpn:
                # update thẳng vào DB
                SanPham.objects.filter(MaSP=sp["MaSP"]).update(GiaNhap=ctpn.GiaNhap)
                # đồng bộ luôn dict
                sp["GiaNhap"] = ctpn.GiaNhap
