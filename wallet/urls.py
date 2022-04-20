from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wallet import views as wallet_views

app_name = 'wallet'

router = DefaultRouter()
router.register('', wallet_views.WalletViewSet, basename="wallet")

urlpatterns = [
    path('', include(router.urls)),
]
