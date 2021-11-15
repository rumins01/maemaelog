from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import TradeLog
from .forms import CreatForm

def dashboard(request):
    posts = TradeLog.objects.filter(name='user').order_by('-update_at')
    return render(request, 'tradelog/dashboard.html', {'posts' : posts})

def create(request):
    if(request.method == 'POST'): 
        form = CreatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tradelog:dashboard')
    else:
        form = CreatForm()
    return render(request, 'tradelog/form_create.html', {'form':form})

def detail(request, tradelog_id):
    tradelog_detail = get_object_or_404(TradeLog, pk=tradelog_id)
    return render(request, 'tradelog/detail.html', {'tradelog_detail':tradelog_detail,})

def update(request, tradelog_id):
    my_tradelog = get_object_or_404(TradeLog, pk=tradelog_id)
    if request.method == 'POST':
        update_form = CreatForm(request.POST, instance = my_tradelog)
        if update_form.is_valid():
            update_form.save()
            return redirect('tradelog:dashboard')
    else:
        update_form = TradeLog(instance=my_tradelog)
    
    return render(request, 'tradelog/update.html', {'update_form' : update_form})

def delete(request, tradelog_id):
    my_tradelog = get_object_or_404(TradeLog, pk=tradelog_id)
    my_tradelog.delete()
    return redirect('tradelog:dashboard')