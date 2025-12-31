from django import forms
from .models import Deposit


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["date", "amount", "rate", "bank"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
