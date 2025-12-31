from django.db import models
from decimal import Decimal
from core.constants import BANK_CHOICES
from users.models import TradingAccount


class Withdrawal(models.Model):
    account = models.ForeignKey(
        TradingAccount,
        on_delete=models.CASCADE,
        related_name="withdrawals"
    )

    date = models.DateField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    bank = models.CharField(max_length=20, choices=BANK_CHOICES)

    capital_before = models.DecimalField(
        max_digits=14, decimal_places=2, editable=False
    )
    capital_after = models.DecimalField(
        max_digits=14, decimal_places=2, editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "created_at"]

    def save(self, *args, **kwargs):
        from core.balances import current_balance  # 👈 lazy import

        if not self.pk:
            self.capital_before = current_balance(self.account)
            self.capital_after = self.capital_before - self.amount

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} | {self.amount} | {self.bank}"
