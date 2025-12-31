from django.contrib import admin
from .models import Deposit


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "account",
        "amount",
        "bank",
        "rate",
        "created_at",
    )

    list_filter = ("bank", "date")
    search_fields = ("bank",)
