from django.db import models

# Create your models here.
class Sunil(models.Model):
    sum = models.IntegerField()

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    address = models.CharField(max_length=500, null=True)
    upi_id = models.CharField(max_length=500, default='')
    logo = models.ImageField(upload_to='hotel_logo_images/', blank=True, null=True)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    gst_status = models.IntegerField(default=0)
    gst_number = models.CharField(max_length=200,null=True)
    discount_status = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True, null=True)
    
    edit_pin = models.CharField(max_length=4, default='0000')
    edit_pin_changed_date = models.DateTimeField(null=True)

class Hotel_Payment(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, null=True)
    amount = models.FloatField()
    bills = models.IntegerField(null=True)
    type = models.CharField(max_length=100)
    date = models.DateField()
    mobile = models.IntegerField(null=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)