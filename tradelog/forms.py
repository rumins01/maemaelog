from django import forms
from django.forms import widgets
from .models import TradeLog
from dal import autocomplete

class CreateForm(forms.ModelForm):
    class Meta:
        model = TradeLog
        fields = '__all__'
        exclude = ['user','code']
        labels = {
            'name' : '종목명',
            'trade_at' : '매매 일자',
            'price' : '매매 단가',
            'amount' : '수량',
            'type' : '매수/매도',
            'account' : '계좌',
            'description' : '매매 이유'
        }
        widgets = {
            'description' : widgets.Textarea(attrs={
                'placeholder' : '매매이유를 입력하세요',
                'cols' : 20,
                'rows' : 10,
                }),
            'name' : autocomplete.ListSelect2(url='tradelog:stockname-autocomplete'),
            'trade_at' : forms.DateInput(format=('%Y/%m/%d')),

        }



