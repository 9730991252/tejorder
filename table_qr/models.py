from django.db import models
from hotel.models import * 
# Create your models here.
class Table_QrCode(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT,null=True)
    url = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    session_id = models.CharField(max_length=500, null=True)
    
    
class Customer_cart(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT,null=True)
    price = models.FloatField()
    total_amount = models.FloatField(default=0)
    qty = models.IntegerField()
    note = models.CharField(max_length=100, null=True)
    accepted_status = models.CharField(default='Pendding', max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True)
    customer_session_id = models.CharField(max_length=500, null=True)
    