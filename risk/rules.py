from decimal import Decimal
from analytics.risk import max_drawdown

MAX_DAILY_LOSS = Decimal("500.00")
MAX_DRAWDOWN = Decimal("-2000.00")


def enforce_prop_rules(account, trade):
    if trade.loss > MAX_DAILY_LOSS:
        raise ValueError("Daily loss limit breached.")

    if max_drawdown(account) < MAX_DRAWDOWN:
        raise ValueError("Maximum drawdown breached.")
