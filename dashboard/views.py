from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.balances import current_balance
from analytics.risk import win_rate, expectancy, max_drawdown


@login_required
def dashboard(request):
    account = request.user.accounts.first()

    return render(request, "dashboard/index.html", {
        "account": account,
        "balance": current_balance(account),
        "win_rate": win_rate(account),
        "expectancy": expectancy(account),
        "drawdown": max_drawdown(account),
    })
