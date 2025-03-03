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
def get_percenteg_amount(percent, without_discount_amount):
    if without_discount_amount:
        return (int(math.floor(float(without_discount_amount))) / 100) * int(percent)
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
    ft_date = date(date.today().year, date.today().month, date.today().day)
    ft_time = time(00, 00, 00)
    from_date = datetime.combine(ft_date, ft_time)
    print(from_date)
    
    day = int(date.today().day) + 1
    
    t_date = date(date.today().year, date.today().month, day)
    t_time = time(00, 00, 00)
    to_date = datetime.combine(t_date, t_time)
    
    total_cash = order_Master.objects.filter(hotel_id=hotel_id, ordered_date__range=[from_date, to_date]).aggregate(Sum('cash_amount'))['cash_amount__sum']
    total_phone_pe = order_Master.objects.filter(hotel_id=hotel_id, ordered_date__range=[from_date, to_date]).aggregate(Sum('phone_pe_amount'))['phone_pe_amount__sum']
    total_pos_machine = order_Master.objects.filter(hotel_id=hotel_id, ordered_date__range=[from_date, to_date]).aggregate(Sum('pos_machine_amount'))['pos_machine_amount__sum']
    discount = order_Master.objects.filter(hotel_id=hotel_id, ordered_date__range=[from_date, to_date]).aggregate(Sum('discount_amount'))['discount_amount__sum']
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