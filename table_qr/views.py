from django.shortcuts import render, redirect
from hotel.models import *
from .models import *
import random
import string  
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Sum, Min, Max
from django.contrib import messages

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
                
                if running_status == 1:
                    return redirect(f'/table_qr/its_running_table/{url}')
                
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
                    messages.error(request,"Successfully deleted")
                    return redirect(f'/table_qr/{url}/')
                
                tp = Hotel_cart.objects.filter(table=table).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
                tp += Customer_cart.objects.filter(table=table).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
                if 'add_rattings'in request.POST:
                    id = request.POST.get('id')
                    ratings = request.POST.get('ratings')
                    
                    ra = Rattings.objects.filter(item_id=id, customer_session_id=session_id).first()
                    if ra is not None:
                        ra.star = ratings
                        ra.save()
                    else:
                        Rattings(
                            item_id=id,
                            customer_session_id=session_id,
                            star=ratings
                        ).save()
                    print('Added ratings')
                    # return redirect(f'/table_qr/its_running_table/{url}')
                item = []
                for i in Item.objects.filter(hotel=hotel, status=1):
                    r = Rattings.objects.filter(item_id=i.id)
                    avrage_r = r.aggregate(Avg('star'))
                    avg = r.filter(customer_session_id=session_id).aggregate(Avg('star'))
                            
                    added_status = 1 if r.filter(item_id=i.id, customer_session_id=session_id).exists() else 0
                    total_r = r.count() 
                    item.append({
                        'id':i.id,
                        'hotel':i.hotel,
                        'marathi_name':i.marathi_name,
                        'english_name':i.english_name,
                        'gst_status':i.gst_status,
                        'discount_status':i.discount_status,
                        'price':i.price,
                        'status':i.status,
                        
                        'average_ratings':(avrage_r['star__avg'] if avrage_r['star__avg'] else 0),
                        'total_r':total_r,
                        
                        '1_star_per':round(float(r.filter(item_id=i.id, star=1).count())*(100/total_r)) if total_r != 0 else 0,
                        '2_star_per':round(float(r.filter(item_id=i.id, star=2).count())*(100/total_r)) if total_r != 0 else 0,
                        '3_star_per':round(float(r.filter(item_id=i.id, star=3).count())*(100/total_r)) if total_r != 0 else 0,
                        '4_star_per':round(float(r.filter(item_id=i.id, star=4).count())*(100/total_r)) if total_r != 0 else 0,
                        '5_star_per':round(float(r.filter(item_id=i.id, star=5).count())*(100/total_r)) if total_r != 0 else 0,
                        
                        'added_status':added_status,
                        'add_avg':avg['star__avg'] if avg['star__avg'] else 0
                    })
                
                context = {
                    'url':url,
                    'table':table,
                    'hotel':hotel,
                    'table_qr':t,
                    'category':Category.objects.filter(hotel=hotel),
                    'item':item,
                    'customer_cart':Customer_cart.objects.filter(table=table, customer_session_id = session_id),
                    'running_status':running_status,
                    'hotel_cart':Hotel_cart.objects.filter(table=table),
                    'count':c.count,
                    'tp':tp
                }
                return render(request, 'table_qr/customer_order.html', context)
            else:
                return redirect('/')
        else:
            return redirect('https://www.google.com/')
    else:
        return redirect('/')
    
@csrf_exempt
def its_running_table(request, url):   
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
                
                if running_status == 0:
                    return redirect('/')
                
                table = t.table
                hotel = table.hotel
                if request.session.has_key('customer_status'):
                    pass
                else:
                    request.session['customer_status'] = 1
                session_id = get_session_id(request)

                
                tp = Hotel_cart.objects.filter(table=table).aggregate(Sum('total_amount'))['total_amount__sum']  or 0
                tp += Customer_cart.objects.filter(table=table).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
                
                cc = Customer_cart.objects.filter(table=table).first()
                h = Hotel_cart.objects.filter(table=table).first()
                first_date = ''
                if cc:
                    first_date =  cc.date
                else:
                    first_date = h.date
                
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
                    'count':c.count,
                    'tp':tp,
                    'first_date':first_date
                }
                return render(request, 'table_qr/its_running_table.html', context)
            else:
                return redirect('/')
        else:
            return redirect('https://www.google.com/')
    else:
        return redirect('/')