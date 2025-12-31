from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum
from trades.models import Trade
from deposits.models import Deposit
from withdrawals.models import Withdrawal

def get_period_range(period):
    today = now().date()

    if period == "day":
        return today, today
    if period == "week":
        return today - timedelta(days=7), today
    if period == "month":
        return today.replace(day=1), today
    if period == "year":
        return today.replace(month=1, day=1), today


def period_summary(period):
    start, end = get_period_range(period)

    profit = Trade.objects.filter(
        date__range=(start, end)
    ).aggregate(Sum("profit"))["profit__sum"] or 0

    loss = Trade.objects.filter(
        date__range=(start, end)
    ).aggregate(Sum("loss"))["loss__sum"] or 0

    deposits = Deposit.objects.filter(
        date__range=(start, end)
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    withdrawals = Withdrawal.objects.filter(
        date__range=(start, end)
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    balance = deposits - withdrawals

    return {
        "profit": profit,
        "loss": loss,
        "deposits": deposits,
        "withdrawals": withdrawals,
        "balance": balance,
        "total": profit - loss + balance,
    }
