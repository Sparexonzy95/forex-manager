from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TradingAccount


@receiver(post_save, sender=User)
def create_trading_account(sender, instance, created, **kwargs):
    if created:
        TradingAccount.objects.create(
            user=instance,
            name="Main Account"
        )
