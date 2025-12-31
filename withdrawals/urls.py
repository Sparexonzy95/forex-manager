from django.urls import path
from .views import (
    list_withdrawals,
    new_withdrawal,
    edit_withdrawal,
    delete_withdrawal,
)

urlpatterns = [
    path("", list_withdrawals),
    path("new", new_withdrawal),
    path("edit/<int:withdrawal_id>/", edit_withdrawal),
    path("delete/<int:withdrawal_id>/", delete_withdrawal),
]
