from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from account.models import Profile
from .models import TradeLog
from .forms import CreateForm
import pandas as pd
import requests
from dal import autocomplete
from datetime import datetime, timedelta

res10 = requests.get('http://marketdata.monple.com/api/').json()

StockNameList = []
StockTickerList = []

for i in range(len(res10)):
    StockNameList.append(res10[i]['name'])
    StockTickerList.append(res10[i]['ticker'])

StockNameTickerDF = pd.DataFrame(zip(StockNameList, StockTickerList), columns=['name', 'code'])


def get_code_by_stock_name(name):
    code1 = StockNameTickerDF[StockNameTickerDF['name'] == name]['code'].values[0]
    return code1



def dashboard(request, tradelog_code=None):
    if not request.user.is_authenticated:
        return redirect("account:log-in")

    context = getDashBoardData(request, tradelog_code)

    return render(request, 'tradelog/dashboard.html', context)


def getDashBoardData(request, tradelog_code=None):
    if tradelog_code == None:
        posts = TradeLog.objects.filter(user=request.user).order_by('-trade_at')
    elif tradelog_code != None:
        posts = TradeLog.objects.filter(user=request.user, code=tradelog_code).order_by('-trade_at')
        # return render(request, 'tradelog/dashboard.html', {'posts': posts})

    #stockrank
    mystock_rank_object = TradeLog.objects.filter(user=request.user)
    mystock_rank_raw1 = pd.DataFrame(mystock_rank_object.values())
    mystock_rank_raw1.loc[mystock_rank_raw1['type'] == 'S', 'amount'] *= -1
    mystock_rank_raw2 = mystock_rank_raw1.groupby('name')['amount'].sum().sort_values(ascending=False)
    mystock_rank_raw3 = mystock_rank_raw2.head(10)

    tradelog_raw = pd.DataFrame((TradeLog.objects.filter(user=request.user)).values())


    # total_sell&buy
    total_sell = format(int(sum(
        tradelog_raw[tradelog_raw['type'] == 'S']['price'] * tradelog_raw[tradelog_raw['type'] == 'S']['amount'])),
                        ',d')
    total_buy = format(int(sum(
        tradelog_raw[tradelog_raw['type'] == 'B']['price'] * tradelog_raw[tradelog_raw['type'] == 'B']['amount'])),
                       ',d')

    # total_asset
    tradelog_raw_minus1 = tradelog_raw
    tradelog_raw_minus1.loc[tradelog_raw['type'] == 'S', 'amount'] *= -1
    tradelog_raw_gb_codeamount = tradelog_raw_minus1.groupby('code').sum()['amount']
    tradelog_raw_codeamount = pd.DataFrame(zip(tradelog_raw_gb_codeamount.index, tradelog_raw_gb_codeamount.values),
                                           columns=['code', 'amount'])
    # d_today_raw = datetime.today()
    # d_today = d_today_raw.strftime('%Y-%m-%d')
    # d_yesterday_raw = d_today_raw + timedelta(days=-2)
    # d_yesterday = d_yesterday_raw.strftime('%Y-%m-%d')
    # d_yyesterday_raw = d_today_raw + timedelta(days=-3)
    # d_yyesterday = d_yyesterday_raw.strftime('%Y-%m-%d')
    daylist_raw = list(requests.get('http://marketdata.monple.com/api/005930/').json()['data'].keys())
    d_yesterday= daylist_raw[len(daylist_raw) - 1]
    d_yyesterday = daylist_raw[len(daylist_raw) - 2]



    code_user = tradelog_raw_codeamount.code
    endprice_yesterday_raw = []
    for i in code_user:
        res = requests.get(f'http://marketdata.monple.com/api/{i}/')
        endprice_yesterday_raw.append(res.json()['data'][d_yesterday])
    endprice_yesterday = pd.DataFrame(zip(code_user, endprice_yesterday_raw), columns=['code', 'price_end'])

    total_asset_raw = tradelog_raw_codeamount.join(endprice_yesterday.set_index('code')['price_end'], on='code')
    total_asset_forcal = sum(total_asset_raw.amount * total_asset_raw.price_end)
    total_asset = format(int(sum(total_asset_raw.amount * total_asset_raw.price_end)), ',d')

    # principal
    tradelog_raw_buy = tradelog_raw[tradelog_raw['type'] == 'B'][['code', 'amount', 'price']]
    tradelog_raw_buy['amountprice'] = tradelog_raw_buy.amount * tradelog_raw_buy.price
    tradelog_raw_buy_gb = tradelog_raw_buy.groupby('code').sum()[['amountprice', 'amount']]
    tradelog_raw_buy_gb['avg'] = tradelog_raw_buy_gb.amountprice / tradelog_raw_buy_gb.amount
    buyavg_raw = pd.DataFrame(zip(tradelog_raw_buy_gb.index, tradelog_raw_buy_gb.avg, ), columns=['code', 'avg'])
    buyavg = buyavg_raw.join(tradelog_raw_codeamount.set_index('code')['amount'], on='code')
    buyavg['avgamount'] = buyavg.avg * buyavg.amount
    principal_raw = sum(buyavg.avgamount)
    principal = format(int(principal_raw), ',d')

    # total_return
    total_return_raw = total_asset_forcal - principal_raw
    total_return = format(int(total_return_raw), ',d')

    # today_return
    total_asset_raw2 = total_asset_raw
    total_asset_raw2.rename(columns={'price_end': 'pricey'}, inplace=True)

    code_user2 = total_asset_raw2.code
    endprice_yyesterday_raw = []
    for i in code_user2:
        res = requests.get(f'http://marketdata.monple.com/api/{i}/')
        endprice_yyesterday_raw.append(res.json()['data'][d_yyesterday])
    endprice_yyesterday = pd.DataFrame(zip(code_user, endprice_yyesterday_raw), columns=['code', 'priceyy'])

    total_return_raw = total_asset_raw2.join(endprice_yyesterday.set_index('code')['priceyy'], on='code')
    today_return = format(int(sum(
        (total_return_raw.amount * total_return_raw.pricey) - (total_return_raw.amount * total_return_raw.priceyy))),
                          ',d')

    # chart
    tradelog_raw_forchart = tradelog_raw_minus1.groupby(['trade_at', 'code']).sum()['amount']
    tradelog_raw_forchart_date = []
    tradelog_raw_forchart_code = []

    for i in tradelog_raw_forchart.index:
        tradelog_raw_forchart_date.append(i[0].strftime('%Y-%m-%d'))
        tradelog_raw_forchart_code.append(i[1])

    tradelog_raw2_forchart = pd.DataFrame(
        zip(tradelog_raw_forchart_date, tradelog_raw_forchart_code, tradelog_raw_forchart.values),
        columns=['date', 'code', 'amount'])

    price_forchart = []
    for i in range(len(tradelog_raw2_forchart)):
        res = requests.get(f'http://marketdata.monple.com/api/{tradelog_raw2_forchart.code[i]}/')
        price_forchart.append(res.json()['data'][tradelog_raw2_forchart.date[i]])

    tradelog_raw2_forchart['price'] = price_forchart
    tradelog_raw2_forchart['amountprice'] = tradelog_raw2_forchart.amount * tradelog_raw2_forchart.price
    tradelog_forchart = tradelog_raw2_forchart.groupby('date').sum()['amountprice']
    tradelog_forchart_df = pd.DataFrame(zip(tradelog_forchart.index, tradelog_forchart.values),
                                        columns=['date', 'amountprice'])

    total_asset_perday = []
    for i in range(len(tradelog_forchart_df)):
        total_asset_perday.append(sum(tradelog_forchart_df['amountprice'][0:i + 1]))
    tradelog_forchart_df['total_asset'] = total_asset_perday
    tradelog_forchart_df_sort = tradelog_forchart_df.sort_values(by='date', ascending=False)

    date_forchart = list(tradelog_forchart_df_sort.date[0:7])
    totalasset_forchart = list(tradelog_forchart_df_sort.total_asset[0:7])
    date_forchart.reverse()
    totalasset_forchart.reverse()

    context = {'mystock_rank': dict(zip(mystock_rank_raw3.index, mystock_rank_raw3.values)),
               "posts": posts,
               'total_sell': total_sell,
               'total_buy': total_buy,
               'total_asset': total_asset,
               'principal': principal,
               'total_return': total_return,
               'today_return': today_return,
               'date_forchart': date_forchart,
               'totalasset_forchart': totalasset_forchart,
               "posts": posts,
               }
    profile = Profile.objects.get(user=request.user)
    if profile:
        context["profile"] = profile

    return context


def create(request):
    form = CreateForm()
    failed_message = ""
    if (request.method == 'POST'):
        tradelog = TradeLog()
        tradelog.user = request.user
        tradelog.code = get_code_by_stock_name(request.POST["name"])
        form = CreateForm(request.POST, instance=tradelog)

        # 가격과 거래량 검사
        price = int(request.POST['price'])
        volume = int(request.POST['amount'])
        if price <= 0 or volume <= 0:
            failed_message = "가격과 거래량은 0이상이어야 합니다."
        else:
            if form.is_valid():
                form.save()
                return redirect('tradelog:dashboard')
            else:
                pass
    else:
        form = CreateForm()
    context = getDashBoardData(request)
    context['failed_message'] = failed_message
    context['isCreate'] = True
    context['form'] = form
    return render(request, 'tradelog/dashboard.html', context)


def detail(request, tradelog_id):
    tradelog_detail = get_object_or_404(TradeLog, pk=tradelog_id)
    return render(request, 'tradelog/detail.html', {'tradelog_detail': tradelog_detail, })


def update(request, tradelog_id):
    context = {}
    failed_message=""
    my_tradelog = get_object_or_404(TradeLog, pk=tradelog_id)
    if request.method == 'POST':
        update_form = CreateForm(request.POST, instance=my_tradelog)

        # 가격과 거래량 검사
        price = int(request.POST['price'])
        volume = int(request.POST['amount'])
        if price <= 0 or volume <= 0:
            failed_message = "가격과 거래량은 0이상이어야 합니다."
        else:
            if update_form.is_valid():
                update_form.save()
                return redirect('tradelog:dashboard')
            else:
                pass
    else:
        update_form = CreateForm(instance=my_tradelog)
    context = getDashBoardData(request)
    context['failed_message'] = failed_message
    context['isUpdate'] = True
    context['update_form'] = update_form
    return render(request, 'tradelog/dashboard.html', context)
    #
    # return render(request, 'tradelog/update.html', context)


def delete(request, tradelog_id):
    my_tradelog = get_object_or_404(TradeLog, pk=tradelog_id)
    my_tradelog.delete()
    return redirect('tradelog:dashboard')

class NameAutocompleteFromList(autocomplete.Select2ListView):
    def get_list(self):
        res3 = requests.get('http://marketdata.monple.com/api/').json()
        NameAutocompleteList = []
        for i in range(len(res3)):
            NameAutocompleteList.append(res3[i]['name'])
        NameAutocompleteList.sort()
        return (NameAutocompleteList)
