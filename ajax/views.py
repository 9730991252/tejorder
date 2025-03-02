from django.http import JsonResponse
from django.shortcuts import render
from hotel.models import *
from table_qr.models import *
from table_qr.views import *
from django.template.loader import render_to_string
from django.db.models import Avg, Sum, Min, Max
import math
# Create your views here.
def add_item_to_customer_cart(request):
    if request.method == 'GET':
        table_id = request.GET['table_id']
        item_id = request.GET['item_id']
        price = request.GET['price']
        qty = request.GET['qty']
        note = request.GET['note']
        session_id = get_session_id(request)
        
        Table_QrCode.objects.filter(table_id=table_id).update(status=1, session_id=session_id)
        c = Customer_cart.objects.filter(table_id=table_id,item_id=item_id).first()
        if c:
            c.qty = qty
            c.price = price
            c.note = note
            c.total_amount=int(qty)*int(math.floor(float(price)))
            c.save()
        else:
            Customer_cart(
                table_id=table_id, 
                item_id=item_id,
                price=price,
                qty=qty,
                note=note,
                total_amount=int(qty)*int(math.floor(float(price))),
                customer_session_id=session_id
            ).save()
    return JsonResponse({'t':'t'})
    
def chang_category_status(request):
    if request.method == 'GET':
        id = request.GET['id']
        category = Category.objects.filter(id=id).first()
        if category.status == 1:
            category.status = 0
            category.save()
        else:
            category.status = 1
            category.save()
    return JsonResponse({'status':category.status})

def chang_teble_status(request):
    if request.method == 'GET':
        id = request.GET['id']
        t = Table.objects.filter(id=id).first()
        if t.status == 1:
            t.status = 0
            t.save()
        else:
            t.status = 1
            t.save()
    t = render_to_string('ajax/chang_teble_status.html', {'t':t})
    return JsonResponse({'t':t})

def add_item_to_hotel_cart_admin(request):
    if request.method == 'GET':
        table_id = request.GET['table_id']
        item_id = request.GET['item_id']
        price = request.GET['price']
        qty = request.GET['qty']
        note = request.GET['note']
        hotel_id = request.GET['hotel_id']
        if note == '':
            note = ' '
        total_amount = request.GET['total_amount']
        Hotel_cart(
            table_id=table_id,
            item_id = item_id,
            price=price,
            qty=qty,
            note=note,
            hotel_id=hotel_id,
            total_amount=total_amount
        ).save()
        amount = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))
        amount = amount['total_amount__sum']
        context={
                'cart':Hotel_cart.objects.filter(table_id=table_id),
        }
        t = render_to_string('ajax/add_item_to_hotel_cart_admin.html', context) 
    return JsonResponse({'t': t,'amount':amount})

def chang_teble_name(request):
    if request.method == 'GET':
        id = request.GET['id']
        name = request.GET['name']
        t = Table.objects.filter(id=id).first()
        t.name = name
        t.save()
        t = Table.objects.filter(id=id).first()
    t = render_to_string('ajax/chang_teble_status.html', {'t':t})
    return JsonResponse({'t':t})

def item_discount_status(request):
    if request.method == 'GET':
        id = request.GET['id']
        i = Item.objects.filter(id=id).first()
        if i.discount_status == 1:
            i.discount_status = 0
            i.save()
        else:
            i.discount_status = 1
            i.save()
    t = render_to_string('ajax/item_gst_status.html', {'item':i,'hotel':i.hotel})
    return JsonResponse({'t':t})

def item_gst_status(request):
    if request.method == 'GET':
        id = request.GET['id']
        i = Item.objects.filter(id=id).first()
        if i.gst_status == 1:
            i.gst_status = 0
            i.save()
        else:
            i.gst_status = 1
            i.save()
    t = render_to_string('ajax/item_gst_status.html', {'item':i,'hotel':i.hotel})
    return JsonResponse({'t':t})

def chang_order_table_id(request):
    if request.method == 'GET':
        old_t = request.GET['old_t']
        new_t = request.GET['new_t']
        
        c = Hotel_cart.objects.filter(table_id=old_t).first()
        c.table_id = new_t
        c.save()
        t = Table.objects.filter(id=new_t).first()
        runing_table = [{'id':t.id,'name':t.name}]
        
        table = []
        for t in Table.objects.filter(status=1):
            status = 'no'        
            c = Hotel_cart.objects.filter(table_id=t.id).exists()
            if c:
                runing_table.append({'id':t.id,'name':t.name})
                status = 'yes'        
            table.append({'id':t.id,'name':t.name,'status':status})
        
    t = render_to_string('ajax/chang_order_table_id.html', {'t':runing_table, 'table':table})
    return JsonResponse({'t':t})

def add_item_to_hotel_cart(request):
    if request.method == 'GET':
        table_id = request.GET['table_id']
        # print('table_id:',table_id)
        item_id = request.GET['item_id']
        # print('item_id:',item_id)
        price = request.GET['price']
        # print('price:',price)
        qty = request.GET['qty']
        # print('qty:',qty)
        total_amount = request.GET['total_amount']
        # print('total_amount:',total_amount)
        note = request.GET['note']
        # print('note:',note)
        waiter_id = request.GET['waiter_id']
        if waiter_id == None:
            waiter_id = ''

        hotel_id = request.GET['hotel_id']
        Hotel_cart(
            table_id=table_id,
            item_id = item_id,
            price=price,
            qty=qty,
            total_amount=total_amount,
            note=note,
            employee_id = waiter_id,
            hotel_id=hotel_id
        ).save()
        amount = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))
        amount = amount['total_amount__sum']
        context={
                'cart':Hotel_cart.objects.filter(table_id=table_id),
        }
        t = render_to_string('ajax/item_to_cart.html', context) 
    return JsonResponse({'t': t,'amount':amount})

def filter_items_by_category(request):
    if request.method == 'GET':
        category_id = request.GET['category_id']
        
        item_id = []
        
        for i in selected_item_category.objects.filter(category_id=category_id, status = 1):
            item_id.append(i.item_id)
        
        items = Item.objects.filter(id__in=item_id, status=1)
        
        context = {
            'item': items,
        }
        t = render_to_string('ajax/filter_items_by_category.html', context)
    return JsonResponse({'t': t})
    
def search_hotel_item(request):
    if request.method == 'GET':
        pass
    
def select_item_category(request):
    if request.method == 'GET':
        c_id = request.GET['c_id']
        item_id = request.GET['item_id']
        category_item = selected_item_category.objects.filter(category_id=c_id,item_id=item_id).first()
        if category_item:
            if category_item.status==0:
                category_item.status = 1
                category_item.save()
            else:
                category_item.status = 0
                category_item.save()
        else:
            selected_item_category(
                category_id=c_id,
                item_id=item_id,
            ).save()
        category=[]
        for c in Category.objects.filter(status=1, hotel_id=category_item.item.hotel_id):
            if selected_item_category.objects.filter(category_id=c.id,item_id=item_id, status=1).exists():
                category.append({'id': c.id,'name':c.name, 'selected_status': 1})
            else:
                category.append({'id': c.id,'name':c.name, 'selected_status': 0})
    context = {
        'category':category
    }
    t = render_to_string('ajax/select_item_category.html', context)
    t1 = render_to_string('ajax/select_item_category1.html', context)
    return JsonResponse({'t':t, 't1':t1})

def select_category_item(request):
    if request.method == 'GET':
        c_id = request.GET['c_id']
        item_id = request.GET['item_id']
        category_item = selected_item_category.objects.filter(category_id=c_id,item_id=item_id).first()
        c = Category.objects.filter(id=c_id).first()
        if category_item:
            if category_item.status==0:
                category_item.status = 1
                category_item.save()
            else:
                category_item.status = 0
                category_item.save()
        else:
            selected_item_category(
                category_id=c_id,
                item_id=item_id,
            ).save()
    context = {
        'c':c
    }
    t = render_to_string('ajax/select_category_item.html', context)
    return JsonResponse({'t':t})
