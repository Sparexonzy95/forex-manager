from decimal import Decimal
from trades.models import Trade


def rebuild_trade_balances(account):
    balance = Decimal("0.00")

    trades = (
        Trade.objects
        .filter(account=account, is_deleted=False)
        .order_by("date", "created_at")
    )

    for trade in trades:
        trade.opening_capital = balance

        pip_value = trade.lot_size * Decimal("100000")

        if trade.sell_rate > trade.buy_rate:
            trade.profit = (trade.sell_rate - trade.buy_rate) * pip_value
            trade.loss = Decimal("0.00")
        else:
            trade.loss = (trade.buy_rate - trade.sell_rate) * pip_value
            trade.profit = Decimal("0.00")

        trade.closing_balance = (
            trade.opening_capital + trade.profit - trade.loss
        )

        balance = trade.closing_balance

        trade.save(update_fields=[
            "opening_capital",
            "profit",
            "loss",
            "closing_balance",
        ])
