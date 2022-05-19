from django.contrib import admin

# Register your models here.
from transaction.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction

    list_display = (
        "id",
        "tx_id",
        "tx_type",
        "result",
        "status",
        "user",
        "created_at",
        "updated_at",
    )
