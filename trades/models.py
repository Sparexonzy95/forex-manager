from decimal import Decimal
from django.db import models
from core.models import SoftDeleteModel
from users.models import TradingAccount
from core.balances import current_balance


class Trade(SoftDeleteModel):
    account = models.ForeignKey(
        TradingAccount,
        on_delete=models.CASCADE,
        related_name="trades",
    )

    date = models.DateField()
    pair = models.CharField(max_length=20)
    lot_size = models.DecimalField(max_digits=6, decimal_places=2)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=4)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=4)

    opening_capital = models.DecimalField(
        max_digits=14, decimal_places=2, editable=False
    )
    profit = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"), editable=False
    )
    loss = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"), editable=False
    )
    closing_balance = models.DecimalField(
        max_digits=14, decimal_places=2, editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "created_at"]

    def save(self, *args, **kwargs):
        if not self.account_id:
            raise ValueError("Trade must have an account before saving.")

        if not self.pk:
            self.opening_capital = current_balance(self.account)

        pip_value = self.lot_size * Decimal("100000")

        if self.sell_rate > self.buy_rate:
            self.profit = (self.sell_rate - self.buy_rate) * pip_value
            self.loss = Decimal("0.00")
        else:
            self.loss = (self.buy_rate - self.sell_rate) * pip_value
            self.profit = Decimal("0.00")

        self.closing_balance = (
            self.opening_capital + self.profit - self.loss
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} | {self.pair}"
