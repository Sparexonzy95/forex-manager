from users.models import TradingAccount


def get_user_account(user):
    account, _ = TradingAccount.objects.get_or_create(
        user=user,
        defaults={"name": "Main Account"},
    )
    return account
