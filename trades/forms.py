from django import forms
from .models import Trade


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ["date", "pair", "lot_size", "buy_rate", "sell_rate"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
