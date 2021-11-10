from django.contrib import admin
from tradelog import models

# Register your models here.
admin.site.register(models.TradeLog)
admin.site.register(models.Account)