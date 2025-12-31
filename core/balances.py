from decimal import Decimal
from django.db.models import Sum


def total_profit(account):
    from trades.models import Trade
    return (
        Trade.objects
        .filter(account=account)
        .aggregate(total=Sum("profit"))["total"]
        or Decimal("0.00")
    )


def total_loss(account):
    from trades.models import Trade
    return (
        Trade.objects
        .filter(account=account)
        .aggregate(total=Sum("loss"))["total"]
        or Decimal("0.00")
    )


def total_deposits(account):
    from deposits.models import Deposit
    return (
        Deposit.objects
        .filter(account=account)
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )


def total_withdrawals(account):
    from withdrawals.models import Withdrawal
    return (
        Withdrawal.objects
        .filter(account=account)
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )


def current_balance(account):
    return (
        total_deposits(account)
        + total_profit(account)
        - total_loss(account)
        - total_withdrawals(account)
    )
