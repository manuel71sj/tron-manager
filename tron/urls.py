from django.urls import path

from tron import views

app_name = 'tron'

urlpatterns = [
    path('contract_create_sample', views.contract_create_sample, name='contract_create_sample'),
    path('mint_nft_sample', views.mint_nft_sample, name='mint_nft_sample'),
    path('address', views.sample, name='tron_sample')
]
