from ..models import SanPham
from decimal import Decimal

class LaiGop:
    def __init__(self, Dot ):
        self.__Dot = Dot
        self.__ds_sp = []

    def init_ds_sp(self, list):
        self.__ds_sp = list

    @property
    def ds_sp(self):
        return self.__ds_sp

    def tinh(self):
        for sp in self.ds_sp:
            gia_ban = sp['GiaBan'] if sp['GiaBan'] is not None else Decimal(0)
            gia_nhap = sp['GiaNhap'] if sp['GiaNhap'] is not None else Decimal(0)

            # Nếu giá nhập = 0 thì không tính lãi
            if gia_nhap == 0:
                sp['LaiGop'] = Decimal(0)
            else:
                laigop = gia_ban - gia_nhap
                thue = Decimal(1) + (Decimal(sp['Thue'] or 0) / Decimal(100))
                sp['LaiGop'] = laigop / thue

                # update thẳng vào DB
                SanPham.objects.filter(MaSP=sp["MaSP"]).update(LaiGop=sp['LaiGop'])
