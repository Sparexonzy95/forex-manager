from django.urls import path
from .views import (
    list_trades,
    new_trade,
    edit_trade,
    delete_trade,
)

urlpatterns = [
    path("", list_trades),
    path("new", new_trade),
    path("edit/<int:trade_id>/", edit_trade),
    path("delete/<int:trade_id>/", delete_trade),
]
