from django.contrib import admin
from .models import Trade

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "pair",
        "lot_size",
        "profit",
        "loss",
        "closing_balance",
    )
    list_filter = ("pair", "date")
    search_fields = ("pair",)
