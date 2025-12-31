from django.db import models
from core.constants import BANK_CHOICES
from users.models import TradingAccount


class Deposit(models.Model):
    account = models.ForeignKey(
        TradingAccount,
        on_delete=models.CASCADE,
        related_name="deposits"
    )

    date = models.DateField()

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    rate = models.DecimalField(
        max_digits=10,
        decimal_places=4
    )

    bank = models.CharField(
        max_length=20,
        choices=BANK_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "created_at"]

    def __str__(self):
        return f"{self.date} | {self.amount} | {self.bank}"
