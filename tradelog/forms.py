from django import forms
from django.forms import widgets
from .models import TradeLog


class CreateForm(forms.ModelForm):
    class Meta:
        model = TradeLog
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'description' : widgets.Textarea(attrs={
                'placeholder' : '매매이유를 입력하세요',
                'cols' : 20,
                'rows' : 10,
                }),
        }



