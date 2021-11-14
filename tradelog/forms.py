from django import forms
from .models import TradeLog


class CreatForm(forms.ModelForm):
    class Meta:
        model = TradeLog
        fields = '__all__'
        

