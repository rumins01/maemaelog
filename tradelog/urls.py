from django.urls import path
from tradelog import views

app_name = 'tradelog'
urlpatterns = [
    # TODO: 매매일지 대시보드 url - https://www.maemaelog.com/nickname/
    # path('<slug:nickname>/', name='dashboard'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('create/', views.create, name='create'),
    path('detail/<int:tradelog_id>', views.detail, name="detail"),
    path('update/<int:tradelog_id>', views.update, name="update"),
    path('delete/<int:tradelog_id>', views.delete, name="delete"),

    
]
