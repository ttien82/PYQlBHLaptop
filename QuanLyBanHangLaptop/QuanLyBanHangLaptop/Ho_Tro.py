from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated



# Các lớp và các class và hàm để thực hiện nhiều tác vụ trùng lặp...
def check_Quyen(user, vai_tro):
    """ Hàm kiểm tra quyền (vai trò)"""
    return (
        user.is_authenticated and
        user.MaQuyen.MaQuyen and
        user.MaQuyen.MaQuyen in vai_tro
    )

class TimKiem:
    """"Lớp hỗ trợ chức năng tìm kiếm ..."""
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        tim = self.request.query_params.get('tim')

        if tim:
            q_obj = Q()
            for field in self.search_fields:
                q_obj |= Q(**{f"{field}__icontains": tim})
            queryset = queryset.filter(q_obj)
        return queryset

class TimKiem_tk:
    """"Lớp hỗ trợ chức năng tìm kiếm ..."""
    search_fields = []

    def tim_kiem_tk(self, tk):
        """Filter thêm theo từ khoá tim trên queryset đã lọc quyền"""
        tim = self.request.query_params.get('tim')
        if tim:
            q_obj = Q()
            for field in self.search_fields:
                q_obj |= Q(**{f"{field}__icontains": tim})
            return tk.filter(q_obj)
        return tk

class VietNamese:
    """Class hỗ trợ chuyển các các cột MaKH, MaNV, TenNv..... sanng Mã khách hàng, Tên ..."""
    vi = {} # map tên tiếng việt

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(self, 'vi')and isinstance(self.vi,dict):
            i = {}
            for k, v in data.items():
                j = self.vi.get(k,k) # nếu có tên tiếng việt thì dùng
                i[j] = v
            return i
        return data

# phân quyền cho tài khoản khác (chưa đăng nhập)
class AllowListRetrieveAnyMixin:
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        if self.action in ['create', 'update']:
            return [IsAuthenticated()]
        if self.action == 'destroy':
            return [IsAuthenticated()]
        return [IsAuthenticated()]