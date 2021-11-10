from django.shortcuts import render
from tradelog.models import TradeLog
import pandas as pd

# Create your views here.

def mystock_rank(request, user_name=1):
    mystock_rank_object = TradeLog.objects.filter(user=user_name)
    mystock_rank_raw1 = pd.DataFrame(mystock_rank_object.values())
    mystock_rank_raw1.loc[mystock_rank_raw1['type'] == 'Sell', 'amount'] *= -1
    mystock_rank_raw2 = mystock_rank_raw1.groupby('name')['amount'].sum().sort_values(ascending=False)
    mystock_rank_raw3 = mystock_rank_raw2.head(10)
    mystock_rank_raw4 = pd.DataFrame(zip(mystock_rank_raw3.index,mystock_rank_raw3.values), columns=['name','amount'])
    # context = { 'mystock_rank' : mystock_rank_raw4 }
    context = {'mystock_rank': dict(zip(mystock_rank_raw3.index, mystock_rank_raw3.values))}
    return render(request, "tradelog/sidebar_right.html", context)


















