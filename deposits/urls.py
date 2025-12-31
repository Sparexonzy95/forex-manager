from django.urls import path
from .views import (
    list_deposits,
    new_deposit,
    edit_deposit,
    delete_deposit,
)

urlpatterns = [
    path("", list_deposits),
    path("new", new_deposit),
    path("edit/<int:deposit_id>/", edit_deposit),
    path("delete/<int:deposit_id>/", delete_deposit),
]
