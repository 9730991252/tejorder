from django.db import models
from sunil.models import  *
from embed_video.fields import EmbedVideoField 
# Create your models here.
class Category(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    order_by = models.IntegerField(default=1)
    
class Item(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT,null=True)
    marathi_name = models.CharField(max_length=100,null=True)
    english_name = models.CharField(max_length=100,null=True)
    gst_status = models.IntegerField(default=0)
    discount_status = models.IntegerField(default=0)
    price = models.FloatField()
    status = models.IntegerField(default=1)
    
class Item_image_and_youtube_url(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT,null=True)
    youtube_url = EmbedVideoField(null=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)


class selected_item_category(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT,null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,null=True)
    status = models.IntegerField(default=1)
    
class Employee(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    
class Table(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    
class Hotel_cart(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT,null=True)
    table = models.ForeignKey(Table,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    price = models.FloatField()
    total_amount = models.FloatField(default=0)
    qty = models.IntegerField()
    note = models.CharField(max_length=100, null=True)
    cook_status = models.CharField(default='Pendding', max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True)
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,null=True,blank=True)
    chef_id = models.CharField(max_length=100,null=True,blank=True)
    session_id = models.CharField(max_length=500, null=True)
    
class order_Master(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT,null=True)
    table=models.ForeignKey(Table,on_delete=models.PROTECT,default=True)
    total_price=models.FloatField(default=0,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    order_filter=models.IntegerField(default=True)
    s_gst = models.FloatField(default=0,null=True)
    c_gst = models.FloatField(default=0,null=True)
    discount_percent = models.IntegerField(default=0)
    discount_amount = models.FloatField(default=0, null=True)
    cash_amount = models.FloatField(default=0, null=True)
    phone_pe_amount = models.FloatField(default=0, null=True)
    pos_machine_amount = models.FloatField(default=0, null=True) 
    paid_status = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    
class order_Detail(models.Model):
    order_master=models.ForeignKey(order_Master,on_delete=models.PROTECT,null=True)
    item=models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    qty = models.IntegerField(default=1)
    price=models.FloatField(default=0,null=True)
    total_price=models.FloatField(default=0,null=True)
    order_filter=models.IntegerField(default=True)
    date = models.DateField(auto_now_add=True,null=True)
    item_name = models.CharField(max_length=100, null=True)
    