from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users.models import TradingAccount
from .models import Deposit
from .forms import DepositForm


@login_required
def list_deposits(request):
    account = request.user.accounts.first()
    deposit_list = Deposit.objects.filter(account=account).order_by("-date")

    paginator = Paginator(deposit_list, 10)
    page_number = request.GET.get("page")
    deposits = paginator.get_page(page_number)

    return render(request, "deposits/list.html", {"deposits": deposits})


@login_required
def new_deposit(request):
    account = request.user.accounts.first()

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.account = account
            deposit.save()
            return redirect("/deposits")
    else:
        form = DepositForm()

    return render(request, "deposits/new.html", {"form": form})


@login_required
def edit_deposit(request, deposit_id):
    account = request.user.accounts.first()
    deposit = get_object_or_404(Deposit, id=deposit_id, account=account)

    if request.method == "POST":
        form = DepositForm(request.POST, instance=deposit)
        if form.is_valid():
            form.save()
            return redirect("/deposits")
    else:
        form = DepositForm(instance=deposit)

    return render(request, "deposits/edit.html", {"form": form})


@login_required
def delete_deposit(request, deposit_id):
    account = request.user.accounts.first()
    deposit = get_object_or_404(Deposit, id=deposit_id, account=account)

    if request.method == "POST":
        deposit.delete()
        return redirect("/deposits")

    return render(request, "deposits/delete.html", {"deposit": deposit})
