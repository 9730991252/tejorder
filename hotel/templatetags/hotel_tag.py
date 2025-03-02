from django import template
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
from sunil.models import *
from hotel.models import *
from table_qr.models import *
register = template.Library()

@register.simple_tag()
def customer_selected_item(category_id):
    category = Category.objects.filter(id=category_id).first()
    item = []
    for i in Item.objects.filter(hotel_id=category.hotel_id):
        selected_status = 0
        if selected_item_category.objects.filter(item_id=i.id,category_id=category.id,status = 1):
            selected_status = 1 
        print(selected_status)
        item.append({'name':i.marathi_name, 'selected_status':selected_status ,'id':i.id})
    return item

@register.simple_tag()
def get_percenteg_amount(percent, without_gst_amount):
    if without_gst_amount:
        return math.floor(int(math.floor(float(without_gst_amount))) / 100) * int(percent)
    else:
        return 0
    
@register.simple_tag()
def remaining_bills(hotel_id):
    h = Hotel.objects.filter(id = hotel_id).first()
    p = Hotel_Payment.objects.filter(hotel_id=h.id).order_by('-id')
    total_bills = p.aggregate(Sum('bills'))['bills__sum']
    if total_bills == None:
        total_bills = 0
    bill = order_Master.objects.filter(hotel_id=h.id).count()
    remaining_bills = (int(total_bills) - int(bill))
    return remaining_bills

@register.inclusion_tag('inclusion_tag/home/customer_qr_code_cart_orders.html')
def customer_qr_code_cart_orders(hotel_id):
    return{'customer_cart':Customer_cart.objects.filter(table__hotel_id=hotel_id)}