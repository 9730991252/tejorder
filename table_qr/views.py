from django.shortcuts import render, redirect
from hotel.models import *
from .models import *
import random
import string  
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def get_session_id(request):
    return request.session.session_key

def generate_nameplate_qrcode(request, id):
    table = Table.objects.filter(id=id).first()
    if table:
        t_qr = Table_QrCode.objects.filter(table_id=table.id).first()
        if t_qr == None:
            code = f"{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{table.id}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}"
            Table_QrCode(
                table_id = table.id,
                url=code,
            ).save()
            t_qr = Table_QrCode.objects.filter(table_id=table.id).first()
        context = {
            'table':table,
            't_qr':t_qr,
            'hotel':table.hotel,
        }
        return render(request, 'table_qr/generate_nameplate_qrcode.html', context)
    else:
        return redirect('/hotel/table_qr/')
    
def generate_table_qrcode(request, id, bg):
    table = Table.objects.filter(id=id).first()
    if table:
        t_qr = Table_QrCode.objects.filter(table_id=table.id).first()
        if t_qr == None:
            code = f"{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{table.id}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}"
            Table_QrCode(
                table_id = table.id,
                url=code,
            ).save()
            t_qr = Table_QrCode.objects.filter(table_id=table.id).first()
        context = {
            'table':table,
            't_qr':t_qr,
            'hotel':table.hotel,
            'bg':bg
        }
        return render(request, 'table_qr/generate_table_qrcode.html', context)
    else:
        return redirect('/hotel/table_qr/')
    
@csrf_exempt
def customer_order(request, url):   
    if url:
        t = Table_QrCode.objects.filter(url=url).first()
        if t:
            if t.active_status == 1:
                c = Table_qr_count.objects.filter(hotel_id=t.table.hotel_id).first()
                if c:
                    c.count += 1
                    c.save()
                else:
                    Table_qr_count(
                        hotel_id = t.table.hotel_id,
                        count=1,
                    ).save()
                c = Table_qr_count.objects.filter(hotel_id=t.table.hotel_id).first()
                
                customer_session = get_session_id(request)
                hc = Hotel_cart.objects.filter(table_id=t.table.id).first()
                cc = Customer_cart.objects.filter(table_id=t.table.id).first()
                if cc:
                    if cc.customer_session_id == customer_session:
                        running_status = 0
                    else:
                        running_status = 1
                elif hc:
                    if hc.session_id == customer_session:
                        running_status = 0
                    else:
                        running_status = 1
                else:
                    running_status = 0
                
                table = t.table
                hotel = table.hotel
                if request.session.has_key('customer_status'):
                    pass
                else:
                    request.session['customer_status'] = 1
                session_id = get_session_id(request)
                if 'delete_order'in request.POST:
                    cart_id = request.POST.get('cart_id')
                    Customer_cart.objects.filter(id=cart_id).delete()
                    return redirect(f'/table_qr/{url}/')
                context = {
                    'url':url,
                    'table':table,
                    'hotel':hotel,
                    'table_qr':t,
                    'category':Category.objects.filter(hotel=hotel),
                    'item':Item.objects.filter(hotel=hotel),
                    'customer_cart':Customer_cart.objects.filter(table=table, customer_session_id = session_id),
                    'running_status':running_status,
                    'hotel_cart':Hotel_cart.objects.filter(table=table),
                    'count':c.count
                }
                return render(request, 'table_qr/customer_order.html', context)
            else:
                return redirect('/')
        else:
            return redirect('https://www.google.com/')
    else:
        return redirect('/')