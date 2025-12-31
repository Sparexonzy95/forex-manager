from decimal import Decimal
from django.db import models
from trades.models import Trade


def win_rate(account):
    total = Trade.objects.filter(account=account).count()
    wins = Trade.objects.filter(account=account, profit__gt=0).count()

    if total == 0:
        return Decimal("0.00")

    return (Decimal(wins) / Decimal(total)) * Decimal("100.00")


def expectancy(account):
    trades = Trade.objects.filter(account=account)

    avg_win = (
        trades.filter(profit__gt=0)
        .aggregate(avg=models.Avg("profit"))["avg"]
        or Decimal("0.00")
    )

    avg_loss = (
        trades.filter(loss__gt=0)
        .aggregate(avg=models.Avg("loss"))["avg"]
        or Decimal("0.00")
    )

    win_rate_pct = win_rate(account)
    win_rate_ratio = win_rate_pct / Decimal("100.00")

    return (
        (win_rate_ratio * avg_win)
        - ((Decimal("1.00") - win_rate_ratio) * avg_loss)
    )


def max_drawdown(account):
    balance = Decimal("0.00")
    peak = Decimal("0.00")
    max_dd = Decimal("0.00")

    for trade in Trade.objects.filter(account=account).order_by("date"):
        balance = trade.closing_balance
        peak = max(peak, balance)
        drawdown = balance - peak
        max_dd = min(max_dd, drawdown)

    return max_dd
