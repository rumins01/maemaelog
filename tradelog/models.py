from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TradeLog(models.Model):
    TRADE_TYPE = [
        ('B', 'Buy'),
        ('S', 'Sell')
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField("stock name", max_length=40)
    code = models.CharField("stock code", max_length=20)
    trade_at = models.DateTimeField("trade date", default=timezone.now())
    price = models.IntegerField("trade price")
    amount = models.IntegerField("trade volume")
    type = models.CharField("trade type", max_length=1, choices=TRADE_TYPE)
    account = models.ForeignKey('Account', on_delete=models.RESTRICT)
    description = models.TextField("trade description")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name


class Account(models.Model):
    BROKERAGE_NAME = [
        ('KW', 'Kiwoom'),
        ('SS', 'Samsung'),
        ('MA', 'Mirae Asset'),
        ('KI', 'Korea Investment'),
        ('DW', 'Daewoo'),
        ('SH', 'Shinhan'),
        ('KM', 'Kookmin'),
        ('SY', 'Shinyoung'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("account name", max_length=40)
    number = models.CharField("account number", max_length=20)
    brokerage = models.CharField("brokerage name", max_length=2, choices=BROKERAGE_NAME)
    fee = models.FloatField("transaction fee")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

