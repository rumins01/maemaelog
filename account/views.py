import datetime
import re

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from account.models import Profile


# Create your views here.

def log_in(request):
    context = {}
    if request.user.is_active:
        profile = Profile.objects.get(user=request.user)
        return redirect("tradelog:home", profile.nickname)
    if request.method == "POST":
        if request.POST.get("username") and request.POST.get("password"):
            username = request.POST.get("username")
            password = request.POST.get("password")
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if username == "admin" or p.match(username) is not None:
                print(f"{username} {password}")
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        profile = Profile.objects.get(user=request.user)
                        context["failed_message"] = "로그인 성공!"
                        return redirect("tradelog:home", profile.nickname)
                        # return render(request, "account/log-in.html", context)

                context["failed_message"] = "잘못된 입력입니다."
            else:
                print(f"{username} isn't email")
                context["failed_message"] = "ID가 이메일 형식이 아닙니다."
        else:
            context["failed_message"] = "잘못된 입력입니다."
        pass
    return render(request, "account/log-in.html", context)


def log_out(request):
    auth.logout(request)
    # if request.method == "POST":

    return redirect("account:log-in")


def sign_in(request):
    context = {}
    if request.method == "POST":
        if (
                request.POST.get("username") and request.POST.get("password") and
                request.POST.get("password") == request.POST.get("password_check")
        ):
            username = request.POST.get("username")
            password = request.POST.get("password")
            password_check = request.POST.get("password_check")
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if p.match(username) is not None:
                try:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=username
                    )
                    if user is not None:
                        context["failed_message"] = "회원가입 성공!"
                        profile = Profile()
                        profile.user = user
                        profile.nickname = f"nick-{format(user.id, '02X')}"
                        profile.save()
                        user.save()
                        auth.login(request, user)
                        return redirect("tradelog:home", profile.nickname)
                        # return render(request, "account/log-in.html", context)
                except:
                    print("회원가입 중 에러 발생")
                context["failed_message"] = "가입할 수 없는 정보가 입력 되어있습니다."
            pass
        else:
            context["failed_message"] = "잘못된 입력입니다."
    return render(request, "account/sign-in.html", context)


def withdraw(request):
    context = {}
    if request.method == "POST":
        print(request.user.username)
        if request.POST.get("password"):
            password = request.POST.get("password")
            user = authenticate(username=request.user.username, password=password)
            if user is not None:
                user.is_active = False
                print(user.is_active)
                user.save()
                auth.logout(request)
                return redirect("account:log-in")
                # return render(request, "account/log-in.html", context)
        context["failed_message"] = "잘못된 입력입니다."

    return render(request, "account/withdraw.html", context)


def password_change(request):
    context = {}
    if request.method == "POST":
        if request.POST.get("password"):
            password = request.POST.get("password")
            user = authenticate(username=request.user.username, password=password)
            if (user is not None and
                    request.POST.get("new_password") == request.POST.get("new_password_check")):
                user.set_password(request.POST.get("new_password"))
                user.save()
                auth.login(request, user)
                return redirect("tradelog:index")
                # return redirect("account:log-in")
        context["failed_message"] = "잘못된 입력입니다."
    return render(request, "account/password-change.html", context)


def profile_edit(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    print(profile.nickname)
    context["profile"] = profile
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.get(user=user)
        nickname = request.POST.get("nickname")
        if not Profile.objects.filter(nickname=nickname).exists():
            profile.nickname = nickname
            if request.POST.get("bio"):
                bio = request.POST.get("bio")
                profile.bio = request.POST.get("bio")
            if request.POST.get("phone_number"):
                phone_number = request.POST.get("phone_number")
                profile.phone_number = phone_number
            if request.POST.get("sex"):
                sex = request.POST.get("sex")
                profile.sex = sex
            profile.save()
            return redirect("account:profile-edit")
        context["failed_message"] = f"{nickname}은 이미 존재하는 닉네임입니다."

    return render(request, "account/profile-edit.html", context)
