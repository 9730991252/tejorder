from django import template
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
import datetime
from datetime import datetime, date, time

from sunil.models import *
from hotel.models import *
from table_qr.models import *
register = template.Library()

@register.simple_tag()
def customer_selected_item_count(category_id):
    return selected_item_category.objects.filter(category_id=category_id,status = 1).count()

@register.simple_tag()
def check_item_image(item_id):
    i = Item_image_and_youtube_url.objects.filter(item_id=item_id).first()
    if i:
        if i.image:
            print('yes')
            return i.image.url
        else:
            print('no')
            return '/static/img/dish.jpg'

@register.simple_tag()
def check_table_running_status_qr_status(table_id):
    qr_status = 0
    if Table_QrCode.objects.filter(table_id=table_id).exists():
        qr_status = 1
    running_status = 0
    if Customer_cart.objects.filter(table_id=table_id).exists():
        running_status = 1
    active_status = 0
    # print(table_id, Table_QrCode.objects.filter(table_id=table_id, active_status=1).first())
    if Table_QrCode.objects.filter(table_id=table_id, active_status=1).exists():
        active_status = 1
    watch_status = 0
    # print(table_id, Table_QrCode.objects.filter(table_id=table_id, active_status=1).first())
    if Table_QrCode.objects.filter(table_id=table_id, watch_and_order_status=1).exists():
        watch_status = 1
    
    return {'qr_status': qr_status, 'running_status': running_status, 'active_status':active_status, 'watch_status':watch_status}
@register.simple_tag()
def get_item_image_and_youtube_url(i_id):
    return Item_image_and_youtube_url.objects.filter(item_id=i_id).first()

@register.simple_tag()
def customer_selected_item(category_id):
    category = Category.objects.filter(id=category_id).first()
    item = []
    for i in Item.objects.filter(hotel_id=category.hotel_id).order_by('marathi_name'):
        selected_status = 0
        if selected_item_category.objects.filter(item_id=i.id,category_id=category.id,status = 1):
            selected_status = 1 
        print(selected_status)
        item.append({'name':i.marathi_name, 'selected_status':selected_status ,'id':i.id})
    return item

@register.simple_tag()
def get_percenteg_amount(percent, discount_amount):
    # print(discount_amount)
    if discount_amount:
        return (int(math.floor(float(discount_amount))) / 100) * int(percent)
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

@register.inclusion_tag('inclusion_tag/hotel/todays_sell.html')
def todays_sell(hotel_id):
    
    item = []
    total_amount = 0
    for i in Item.objects.filter(hotel_id=hotel_id):
        qty = order_Detail.objects.filter(item_id=i.id,date__range=[date.today(), date.today()] ).aggregate(Sum('qty'))['qty__sum']
        total_price = order_Detail.objects.filter(item_id=i.id, date__range=[date.today(), date.today()]).aggregate(Sum('total_price'))['total_price__sum']
        if total_price == None:
            total_price = 0
        total_amount += total_price
        if qty != None:
            item.append({'name':i.marathi_name, 'qty':qty, 'total_price':total_price})        

    from_date = date.today()
    to_date = date.today()
    
    total_cash = order_Master.objects.filter(hotel_id=hotel_id, date__range=[from_date, to_date]).aggregate(Sum('cash_amount'))['cash_amount__sum']
    total_phone_pe = order_Master.objects.filter(hotel_id=hotel_id, date__range=[from_date, to_date]).aggregate(Sum('phone_pe_amount'))['phone_pe_amount__sum']
    total_pos_machine = order_Master.objects.filter(hotel_id=hotel_id, date__range=[from_date, to_date]).aggregate(Sum('pos_machine_amount'))['pos_machine_amount__sum']
    discount = order_Master.objects.filter(hotel_id=hotel_id, date__range=[from_date, to_date]).aggregate(Sum('discount_amount'))['discount_amount__sum']
    hotel = Hotel.objects.filter(id=hotel_id).first()
    return{
        'item':item,
        'total_amount':total_amount,
        'total_cash':total_cash,
        'total_phone_pe':total_phone_pe,
        'total_pos_machine':total_pos_machine,
        'discount':discount,
        'hotel':hotel
        
        }