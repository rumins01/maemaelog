from django.urls import include
from django.urls import path

app_name = 'account'
urlpatterns = [
    # TODO: 랜딩 페이지 뷰 및 연결 url - https://www.maemaelog.com/
    # path('', views.landing_page, name='landing-page'),

    # TODO: 로그인 상태에서 개인 프로필 페이지 url - https://www.maeamelog.com/nickname/profile/
    # path('<slug:nickname>/profile/', views.user_profile, name='user-profile'),
]
