from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wallet import views as wallet_views

app_name = "wallet"

router = DefaultRouter()
router.register("", wallet_views.WalletViewSet, basename="wallet")

urlpatterns = [
    path("", include(router.urls)),
    path("generate", wallet_views.create_wallet, name="generate_wallet"),
    path(
        "generate_with_passphrase",
        wallet_views.create_wallet_with_passphrase,
        name="generate_wallet_with_passphrase",
    ),
    path("use_wallet/<int:pk>", wallet_views.use_wallet, name="use_wallet"),
    path("test_session", wallet_views.test_session, name="test_session"),
]
