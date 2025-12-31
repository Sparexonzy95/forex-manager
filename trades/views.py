from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from core.utils import get_user_account
from core.recalculate import rebuild_trade_balances
from risk.rules import enforce_prop_rules

from .models import Trade
from .forms import TradeForm


@login_required
def list_trades(request):
    account = get_user_account(request.user)
    trade_list = Trade.objects.filter(
        account=account,
        is_deleted=False
    ).order_by("-date")

    paginator = Paginator(trade_list, 10)
    page_number = request.GET.get("page")
    trades = paginator.get_page(page_number)

    return render(request, "trades/list.html", {"trades": trades})


@login_required
def new_trade(request):
    account = get_user_account(request.user)

    if request.method == "POST":
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.account = account

            enforce_prop_rules(account, trade)

            trade.save()
            rebuild_trade_balances(account)

            return redirect("/trades")
    else:
        form = TradeForm()

    return render(request, "trades/new.html", {"form": form})


@login_required
def edit_trade(request, trade_id):
    account = get_user_account(request.user)
    trade = get_object_or_404(
        Trade,
        id=trade_id,
        account=account,
        is_deleted=False
    )

    if request.method == "POST":
        form = TradeForm(request.POST, instance=trade)
        if form.is_valid():
            form.save()
            rebuild_trade_balances(account)
            return redirect("/trades")
    else:
        form = TradeForm(instance=trade)

    return render(request, "trades/edit.html", {"form": form})


@login_required
def delete_trade(request, trade_id):
    account = get_user_account(request.user)
    trade = get_object_or_404(
        Trade,
        id=trade_id,
        account=account,
        is_deleted=False
    )

    if request.method == "POST":
        trade.soft_delete()
        rebuild_trade_balances(account)
        return redirect("/trades")

    return render(request, "trades/delete.html", {"trade": trade})
