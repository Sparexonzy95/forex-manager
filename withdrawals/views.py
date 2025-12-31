from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users.models import TradingAccount
from .models import Withdrawal
from .forms import WithdrawalForm
from core.utils import get_user_account

@login_required
def list_withdrawals(request):
    account = request.user.accounts.first()
    withdrawal_list = Withdrawal.objects.filter(account=account).order_by("-date")

    paginator = Paginator(withdrawal_list, 10)  # 10 per page
    page_number = request.GET.get("page")
    withdrawals = paginator.get_page(page_number)

    return render(
        request,
        "withdrawals/list.html",
        {"withdrawals": withdrawals}
    )


@login_required
def new_withdrawal(request):
    account = request.user.accounts.first()

    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.account = account
            withdrawal.save()
            return redirect("/withdrawals")
    else:
        form = WithdrawalForm()

    return render(
        request,
        "withdrawals/new.html",
        {"form": form}
    )


@login_required
def edit_withdrawal(request, withdrawal_id):
    account = request.user.accounts.first()
    withdrawal = get_object_or_404(
        Withdrawal,
        id=withdrawal_id,
        account=account
    )

    if request.method == "POST":
        form = WithdrawalForm(request.POST, instance=withdrawal)
        if form.is_valid():
            form.save()
            return redirect("/withdrawals")
    else:
        form = WithdrawalForm(instance=withdrawal)

    return render(
        request,
        "withdrawals/edit.html",
        {"form": form}
    )


@login_required
def delete_withdrawal(request, withdrawal_id):
    account = get_user_account(request.user)
    withdrawal = get_object_or_404(
        Withdrawal,
        id=withdrawal_id,
        account=account
    )

    if request.method == "POST":
        withdrawal.delete()
        return redirect("/withdrawals")

    return render(
        request,
        "withdrawals/delete.html",
        {"withdrawal": withdrawal}
    )
