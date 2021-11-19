from django.shortcuts import render
from tradelog.models import TradeLog
import pandas as pd
import requests
from datetime import datetime

# Create your views here.

def mystock_rank(request):
    mystock_rank_object = TradeLog.objects.filter(user=request.user)
    mystock_rank_raw1 = pd.DataFrame(mystock_rank_object.values())
    mystock_rank_raw1.loc[mystock_rank_raw1['type'] == 'S', 'amount'] *= -1
    mystock_rank_raw2 = mystock_rank_raw1.groupby('name')['amount'].sum().sort_values(ascending=False)
    mystock_rank_raw3 = mystock_rank_raw2.head(10)
    context = {'mystock_rank': dict(zip(mystock_rank_raw3.index, mystock_rank_raw3.values))}
    return render(request, "tradelog/sidebar_right.html", context)


def KPI(request):
    tradelog_raw = pd.DataFrame((TradeLog.objects.filter(user=request.user)).values())

    #total_sell&buy
    total_sell = format(int(sum(tradelog_raw[tradelog_raw['type'] == 'S']['price'] * tradelog_raw[tradelog_raw['type'] == 'S']['amount'])),',d')
    total_buy = format(int(sum(tradelog_raw[tradelog_raw['type'] == 'B']['price'] * tradelog_raw[tradelog_raw['type'] == 'B']['amount'])),',d')

    # total_asset
    tradelog_raw_minus1 = tradelog_raw
    tradelog_raw_minus1.loc[tradelog_raw['type'] == 'S', 'amount'] *= -1
    tradelog_raw_gb_codeamount = tradelog_raw_minus1.groupby('code').sum()['amount']
    tradelog_raw_codeamount = pd.DataFrame(zip(tradelog_raw_gb_codeamount.index, tradelog_raw_gb_codeamount.values), columns=['code', 'amount'])

    code_user = tradelog_raw_codeamount.code
    endprice_yesterday_raw = []
    for i in code_user:
        res = requests.get(f'http://marketdata.monple.com/api/{i}/')
        endprice_yesterday_raw.append(res.json()['data']['1999-05-18'])
    endprice_yesterday = pd.DataFrame(zip(code_user, endprice_yesterday_raw), columns=['code', 'price_end'])

    total_asset_raw = tradelog_raw_codeamount.join(endprice_yesterday.set_index('code')['price_end'], on='code')
    total_asset_forcal = sum(total_asset_raw.amount * total_asset_raw.price_end)
    total_asset = format(int(sum(total_asset_raw.amount * total_asset_raw.price_end)),',d')

    # principal
    tradelog_raw_buy = tradelog_raw[tradelog_raw['type'] == 'B'][['code', 'amount', 'price']]
    tradelog_raw_buy['amountprice'] = tradelog_raw_buy.amount * tradelog_raw_buy.price
    tradelog_raw_buy_gb = tradelog_raw_buy.groupby('code').sum()[['amountprice', 'amount']]
    tradelog_raw_buy_gb['avg'] = tradelog_raw_buy_gb.amountprice / tradelog_raw_buy_gb.amount
    buyavg_raw = pd.DataFrame(zip(tradelog_raw_buy_gb.index, tradelog_raw_buy_gb.avg, ), columns=['code', 'avg'])
    buyavg = buyavg_raw.join(tradelog_raw_codeamount.set_index('code')['amount'], on='code')
    buyavg['avgamount'] = buyavg.avg * buyavg.amount
    principal_raw = sum(buyavg.avgamount)
    principal = format(int(principal_raw),',d')

    # total_return
    total_return_raw = total_asset_forcal - principal_raw
    total_return = format(int(total_return_raw),',d')

    # today_return
    total_asset_raw2 = total_asset_raw
    total_asset_raw2.rename(columns={'price_end': 'pricey'}, inplace=True)

    code_user2 = total_asset_raw2.code
    endprice_yyesterday_raw = []
    for i in code_user2:
        res = requests.get(f'http://marketdata.monple.com/api/{i}/')
        endprice_yyesterday_raw.append(res.json()['data']['1999-05-17'])
    endprice_yyesterday = pd.DataFrame(zip(code_user, endprice_yyesterday_raw), columns=['code', 'priceyy'])

    total_return_raw = total_asset_raw2.join(endprice_yyesterday.set_index('code')['priceyy'], on='code')
    today_return = format(int(sum((total_return_raw.amount * total_return_raw.pricey) - (total_return_raw.amount * total_return_raw.priceyy))),',d')

    #chart
    tradelog_raw_forchart = tradelog_raw_minus1.groupby(['trade_at', 'code']).sum()['amount']
    tradelog_raw_forchart_date = []
    tradelog_raw_forchart_code = []

    for i in tradelog_raw_forchart.index:
        tradelog_raw_forchart_date.append(i[0].strftime('%Y-%m-%d'))
        tradelog_raw_forchart_code.append(i[1])

    tradelog_raw2_forchart = pd.DataFrame(zip(tradelog_raw_forchart_date, tradelog_raw_forchart_code, tradelog_raw_forchart.values), columns=['date', 'code', 'amount'])

    price_forchart = []
    for i in range(len(tradelog_raw2_forchart)):
        res = requests.get(f'http://marketdata.monple.com/api/{tradelog_raw2_forchart.code[i]}/')
        price_forchart.append(res.json()['data'][tradelog_raw2_forchart.date[i]])

    tradelog_raw2_forchart['price'] = price_forchart
    tradelog_raw2_forchart['amountprice'] = tradelog_raw2_forchart.amount * tradelog_raw2_forchart.price
    tradelog_forchart = tradelog_raw2_forchart.groupby('date').sum()['amountprice']
    tradelog_forchart_df = pd.DataFrame(zip(tradelog_forchart.index, tradelog_forchart.values), columns=['date', 'amountprice'])

    total_asset_perday = []
    for i in range(len(tradelog_forchart_df)):
        total_asset_perday.append(sum(tradelog_forchart_df['amountprice'][0:i + 1]))
    tradelog_forchart_df['total_asset'] = total_asset_perday
    tradelog_forchart_df_sort = tradelog_forchart_df.sort_values(by = 'date', ascending=False)

    date_forchart = list(tradelog_forchart_df_sort.date[0:7])
    totalasset_forchart = list(tradelog_forchart_df_sort.total_asset[0:7])
    date_forchart.reverse()
    totalasset_forchart.reverse()

    context = {'total_sell' : total_sell,
               'total_buy' : total_buy,
               'total_asset' : total_asset,
               'principal' : principal,
               'total_return' : total_return,
               'today_return' : today_return,
               'date_forchart' : date_forchart,
               'totalasset_forchart' : totalasset_forchart,
               }

    return render(request, "tradestats/sidebar_left.html",context)



d_today_raw = datetime.today()
d_today = d_today_raw.strftime('%Y-%m-%d')