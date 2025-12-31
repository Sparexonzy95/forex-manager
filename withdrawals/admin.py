from django.contrib import admin
from .models import Withdrawal


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "account",
        "amount",
        "bank",
        "capital_before",
        "capital_after",
        "created_at",
    )

    list_filter = ("bank", "date")
    search_fields = ("bank",)
    readonly_fields = ("capital_before", "capital_after", "created_at")
