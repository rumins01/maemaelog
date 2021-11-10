from django.contrib import admin
<<<<<<< HEAD
from tradelog import models

# Register your models here.
admin.site.register(models.TradeLog)
admin.site.register(models.Account)
=======
from .models import TradeLog, Account


# Register your models here.
admin.site.register(TradeLog)
admin.site.register(Account)

>>>>>>> 1cbcb50f04f466ce069207cf3699714475267179
