from django.urls import include
from django.urls import path

from account import views


app_name = "account"
urlpatterns = [
    # TODO: 랜딩 페이지 뷰 및 연결 url - https://www.maemaelog.com/
    # path('', views.landing_page, name='landing-page'),

    # TODO: 로그인 상태에서 개인 프로필 페이지 url - https://www.maeamelog.com/nickname/profile/
    # path('<slug:nickname>/profile/', views.user_profile, name='user-profile'),
    path("", views.index, name="home"),
    path("register/", views.register, name="register"),
    path("log-in/", views.log_in, name="log-in"),
    path("log-out/", views.log_out, name="log-out"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("password/change", views.password_change, name="password-change"),
    path("profile-edit", views.profile_edit, name="profile-edit"),
    path("account-list", views.account_list, name="account-list"),
    path("create-account", views.create_account, name="create-account"),
    path("<int:account_id>/update-account/", views.update_account, name="update-account"),
    path("<int:account_id>/delete-account/", views.delete_account, name="delete-account"),

]
