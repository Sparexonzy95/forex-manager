from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("", include("users.urls")),
    path("trades/", include("trades.urls")),
    path("deposits/", include("deposits.urls")),
    path("withdrawals/", include("withdrawals.urls")),
]
