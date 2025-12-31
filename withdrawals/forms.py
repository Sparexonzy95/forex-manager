from django import forms
from .models import Withdrawal


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["date", "amount", "bank"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
