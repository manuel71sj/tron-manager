from django.contrib import admin

# Register your models here.
from contract.models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    model = Contract

    list_display = (
        "id",
        "tx",
        "wallet",
        "contract_address",
        "trc_type",
        "name",
        "symbol",
    )
