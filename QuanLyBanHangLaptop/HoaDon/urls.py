
from rest_framework.routers import DefaultRouter
from .views import DonHangViewSet, ChiTietDonHangViewSet

router = DefaultRouter()
router.register(r'cthoadon', ChiTietDonHangViewSet, basename='cthoadon')

router.register(r'', DonHangViewSet,basename='donhang')
urlpatterns = router.urls
