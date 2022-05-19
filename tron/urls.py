from django.urls import path

from tron import views

app_name = "tron"

urlpatterns = [
    path("mint_nft", views.mint_nft, name="mint_nft"),
    path("contract_create", views.contract_create, name="contract_create"),
    path("example_view", views.example_view, name="example_view"),
]
