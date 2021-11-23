from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

import tradelog
from .models import TradeLog
from .forms import CreateForm



def dashboard(request, tradelog_code=None):
    if request.user.is_authenticated:
        if tradelog_code == None:
            posts = TradeLog.objects.filter(user=request.user).order_by()
        elif tradelog_code != None:
            posts = TradeLog.objects.filter(user=request.user, code=tradelog_code).order_by()
        return render(request, 'tradelog/dashboard.html', {'posts': posts})
    else:
        return redirect("account:log-in")



def create(request):
    form = CreateForm()
    context = {}
    if(request.method == 'POST'):
        tradelog = TradeLog()
        tradelog.user = request.user
        form = CreateForm(request.POST, instance=tradelog)
        
        # 가격과 거래량 검사
        price = int(request.POST['price'])
        volume = int(request.POST['amount'])
        if price <= 0 or volume <= 0:
            context["failed_message"] = "가격과 거래량은 0이상이어야 합니다."
        else:
            if form.is_valid():
                form.save()
                return redirect('tradelog:dashboard')
            else:
                pass
    else:
        pass
    
    context['form'] = form
    return render(request, 'tradelog/form_create.html', context)



def detail(request, tradelog_id):
    tradelog_detail = get_object_or_404(TradeLog, pk=tradelog_id)
    return render(request, 'tradelog/detail.html', {'tradelog_detail':tradelog_detail,})



def update(request, tradelog_id):
    context = {}
    my_tradelog = get_object_or_404(TradeLog, pk=tradelog_id)
    if request.method == 'POST':
        update_form = CreateForm(request.POST, instance = my_tradelog)
        
        # 가격과 거래량 검사
        price = int(request.POST['price'])
        volume = int(request.POST['amount'])
        if price <= 0 or volume <= 0:
            context["failed_message"] = "가격과 거래량은 0이상이어야 합니다."
        else:
            if update_form.is_valid():
                update_form.save()
                return redirect('tradelog:dashboard')
            else:
                pass
    else:
        update_form = CreateForm(instance=my_tradelog)

    context['update_form'] = update_form
    return render(request, 'tradelog/update.html', context)



def delete(request, tradelog_id):
    my_tradelog = get_object_or_404(TradeLog, pk=tradelog_id)
    my_tradelog.delete()
    return redirect('tradelog:dashboard')