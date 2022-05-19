# Register your models here.
from django.contrib import admin

from wallet.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    model = Wallet

    list_display = ("id", "user", "address", "active")
