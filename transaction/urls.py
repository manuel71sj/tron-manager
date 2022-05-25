from django.urls import path

from transaction import views

app_name = "trx"

urlpatterns = [
    path("send_tron", views.send_tron, name="send_tron"),
    path("get_result", views.get_trx_result, name="get_result"),
    path("get_trx_by_hash", views.get_trx_by_hash, name="get_trx_by_hash"),
    path("get_message_by_hash", views.get_message_by_hash, name="get_message_by_hash"),
]
