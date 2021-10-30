from django.shortcuts import render


# Create your views here.

def log_in(request):
    return render(request, "account/log-in.html")


def log_out(request):
    return render(request, "account/log-out.html")


def sign_in(request):
    return render(request, "account/sign-in.html")
