from django.shortcuts import render, redirect
from .models import *
from table_qr.models import *
from sunil.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Sum, Min, Max
import math
from datetime import date
from PIL import Image
import io
from datetime import datetime, date, time
from django.core.paginator import Paginator
from django.contrib import messages 

# Create your views here.
@csrf_exempt
def hotel_home(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()

        context={
            'hotel':hotel
        }
        return render(request, 'hotel/hotel_home.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def edit_bill(request, id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        om = order_Master.objects.filter(id=id).first()
        ord = order_Detail.objects.filter(order_master=om)
        amount = ord.aggregate(Sum('total_price'))['total_price__sum']
        if 'Delete'in request.POST:
            od_id = request.POST.get('cart_id')
            od = order_Detail.objects.filter(id=od_id).first()
            om.total_price -= od.total_price
            om.cash_amount = 0
            om.phone_pe_amount = 0
            om.pos_machine_amount = 0
            om.save()
            od.delete()
            return redirect(f'/hotel/edit_bill/{id}')
        context={
            'hotel':hotel,
            'om':order_Master.objects.filter(id=id).first(),
            'ord':ord,
            'amount':amount,
            'category':Category.objects.filter(status=1),
            'item':Item.objects.filter(status=1),
        }
        return render(request, 'hotel/edit_bill.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def report(request):

    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        item = []
        from_date = ''
        to_date = ''
        total_amount = 0
        total_cash = 0
        total_phone_pe = 0
        total_pos_machine = 0
        discount = 0
        if 'search_report' in request.POST:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            total_amount = 0
            for i in Item.objects.filter(hotel_id=hotel.id):
                qty = order_Detail.objects.filter(item_id=i.id,date__range=[from_date, to_date] ).aggregate(Sum('qty'))['qty__sum']
                total_price = order_Detail.objects.filter(item_id=i.id, date__range=[from_date, to_date]).aggregate(Sum('total_price'))['total_price__sum']
                
                if total_price == None:
                    total_price = 0
                total_amount += total_price
                if qty != None:
                    item.append({'name':i.marathi_name, 'qty':qty, 'total_price':total_price})  
                          
            total_cash = order_Master.objects.filter(date__range=[from_date, to_date], hotel_id=hotel.id).aggregate(Sum('cash_amount'))['cash_amount__sum']
            total_phone_pe = order_Master.objects.filter(date__range=[from_date, to_date], hotel_id=hotel.id).aggregate(Sum('phone_pe_amount'))['phone_pe_amount__sum']
            total_pos_machine = order_Master.objects.filter(date__range=[from_date, to_date], hotel_id=hotel.id).aggregate(Sum('pos_machine_amount'))['pos_machine_amount__sum']
            discount = order_Master.objects.filter(date__range=[from_date, to_date], hotel_id=hotel.id).aggregate(Sum('discount_amount'))['discount_amount__sum']

        context={
            'hotel':hotel,
            'item':item,
            'from_date':from_date,
            'to_date':to_date,
            'total_amount':total_amount,
            'total_cash':total_cash,                
            'total_phone_pe':total_phone_pe,                
            'total_pos_machine':total_pos_machine,
            'discount':discount,
        }
        return render(request, 'hotel/report.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def table_qr(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        t = Table.objects.filter(hotel_id=hotel.id)
        if 'reset_table'in request.POST:
            id = request.POST.get('id')
            t = Table.objects.filter(id=id).first()
            Customer_cart.objects.filter(table_id=id).delete()
            messages.success(request,f"{t.name} Reseted SuccessFully.")
            return redirect('/hotel/table_qr/')
        context={
            'hotel':hotel,
            'table':t
            
        }
        return render(request, 'hotel/table_qr.html', context)
    else:
        return redirect('login')
    
def complate_order(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        if hotel:
            
            if 'cancel_bill'in request.POST:
                order_filter = request.POST.get('order_filter')
                om = order_Master.objects.filter(order_filter=order_filter).first()
                om.status = 0
                om.save()
                return redirect('complate_order')
            order_master = []
            for b in order_Master.objects.filter(hotel_id=hotel.id).order_by('-id'):
                cancel_btn_show_status = 0
                order_details = order_Detail.objects.filter(order_filter=b.order_filter).first()
                if order_details:
                    if order_details.date == date.today():
                        cancel_btn_show_status = 1
                order_master.append({
                    'id': b.id,
                    'order_filter': b.order_filter,
                    'total_price': b.total_price,
                    'ordered_date': b.ordered_date,
                    'status':b.status,
                    'cancel_btn_show_status':cancel_btn_show_status
                })
            
            paginator = Paginator(order_master, per_page=100)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
        context={
            'hotel':hotel,
            'order_master':page_obj
        }
        return render(request, 'hotel/complate_order.html', context)
    else:
        return redirect('/login/')
     
@csrf_exempt
def profile(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        if 'save_profile'in request.POST:
            owner_name = request.POST.get('owner_name')
            hotel_name = request.POST.get('hotel_name')
            hotel_address = request.POST.get('hotel_address')
            pin = request.POST.get('pin')
            upi_id = request.POST.get('upi_id')
            gst_number = request.POST.get('gst_number')
            logo_img = request.FILES.get('logo_img')
            hotel.owner_name = owner_name
            hotel.hotel_name = hotel_name
            hotel.address = hotel_address
            hotel.pin = pin
            hotel.upi_id = upi_id
            hotel.gst_number = gst_number
            hotel.save()
            if logo_img is not None:
                compressed_image = compress_image(logo_img)
                hotel.logo.save(logo_img.name[:-5]+'.webp', compressed_image, save=True)
            return redirect('profile')
        context={
            'hotel':hotel
        }
        return render(request, 'hotel/profile.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def complate_view_order(request,order_filter):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        scroll_status = 0
        if hotel:
            bill_status = 0
            om = order_Master.objects.filter(order_filter=order_filter, hotel_id=hotel.id).first()

            if request.POST:
                type = request.POST.get('type')
                if type == 'chang_bill_paid_status':
                    om.paid_status = 1
                    om.save()
            without_gst_amount = order_Detail.objects.filter(order_filter=order_filter, item__gst_status=0).aggregate(Sum('total_price'))['total_price__sum']
            discount_amount = order_Detail.objects.filter(order_filter=order_filter, item__discount_status=1).aggregate(Sum('total_price'))['total_price__sum']
            
            total_price = om.total_price
            total_price -= om.discount_amount
            total_price += om.s_gst
            total_price += om.s_gst
            if 'select_discount'in request.POST:
                percent = request.POST.get('percent')
                am = (int(math.floor(float(discount_amount))) / 100) * int(percent)
                om.discount_percent = percent
                om.discount_amount = am
                om.cash_amount=om.total_price
                om.phone_pe_amount=0
                om.pos_machine_amount=0
                om.save()
                total_price = om.total_price
                total_price -= om.discount_amount
                total_price += om.s_gst
                total_price += om.c_gst
                om.cash_amount = total_price
                om.save()
                scroll_status = 1
                return redirect('complate_view_order', order_filter)
            if 'add_phone_pe_amount'in request.POST:
                phone_pe_amount = request.POST.get('phonepe_amount')
                om.phone_pe_amount = phone_pe_amount
                om.cash_amount -= float(phone_pe_amount)
                om.save()
                om = order_Master.objects.filter(order_filter=order_filter).first()
                return redirect('complate_view_order', order_filter)
            if 'edit_phone_pe_amount'in request.POST:
                phone_pe_amount = request.POST.get('phonepe_amount')
                old_amount = om.phone_pe_amount
                if old_amount > float(phone_pe_amount):
                    om.cash_amount +=  float(old_amount) - float(phone_pe_amount)
                else:
                    om.cash_amount -= float(phone_pe_amount) - float(old_amount) 
                om.phone_pe_amount = phone_pe_amount
                om.save()
                om = order_Master.objects.filter(order_filter=order_filter).first()
                om.save()
                return redirect('complate_view_order', order_filter)
            if 'add_pos_machine_amount'in request.POST:
                pos_machine_amount = request.POST.get('pos_machine_amount')
                om.pos_machine_amount = pos_machine_amount
                om.cash_amount -= float(pos_machine_amount)
                om.save()
                return redirect('complate_view_order', order_filter)
            if 'edit_pos_machine_amount'in request.POST:
                pos_machine_amount = request.POST.get('pos_machine_amount')
                old_amount = om.pos_machine_amount
                if old_amount > float(pos_machine_amount):
                    om.cash_amount +=  float(old_amount) - float(pos_machine_amount)
                else:
                    om.cash_amount -= float(pos_machine_amount) - float(old_amount) 
                om.pos_machine_amount = pos_machine_amount
                om.save()
                om = order_Master.objects.filter(order_filter=order_filter).first()
                om.save()
                return redirect('complate_view_order', order_filter)
            
        context={
            'hotel':hotel,
            'om':om,
            'bill_status':bill_status,
            'order_detail':order_Detail.objects.filter(order_master=om.id),
            'without_gst_amount':without_gst_amount,
            'scroll_status':scroll_status,
            'total_price':math.floor(total_price),
            'discount_amount':discount_amount
            
        }
        return render(request, 'hotel/complate_view_order.html', context)
    else:
        return redirect('/login/')
    
@csrf_exempt
def view_order(request, table_id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        if hotel:
            amount = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))
            amount = amount['total_amount__sum']
            if amount == None:
                amount = 0
            if 'Delete'in request.POST:
                cart_id = request.POST.get('cart_id')
                Hotel_cart.objects.filter(id=cart_id).delete()
                return redirect(f'/hotel/view_order/{table_id}')
            if 'complete_order'in request.POST:
                order_filter = (int(order_Master.objects.filter(hotel_id=hotel.id).count()) + 1)
                
                comolete_order(order_filter, table_id, hotel.id)
                return redirect(f'/hotel/complate_view_order/{order_filter}')
        context={
            'hotel':hotel,
            'cart':Hotel_cart.objects.filter(table_id=table_id),
            'amount':amount,
            'item':Item.objects.filter(status=1,hotel_id=hotel.id).order_by('marathi_name'),
            'table':Table.objects.get(id=table_id),
            'category':Category.objects.filter(status=1,hotel_id=hotel.id).order_by('-order_by')
        }
        return render(request, 'hotel/view_order.html', context)
    else:
        return redirect('login')
    
def comolete_order(order_filter, table_id, hotel_id):
    hotel = Hotel.objects.filter(id=hotel_id).first()
    t =Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))['total_amount__sum']
    if t != None:
        ta = Hotel_cart.objects.filter(table_id=table_id, item__gst_status=0).aggregate(Sum('total_amount'))['total_amount__sum']
        if ta != None:
            t -= ta
        
    gst = (t / 100) * 5
    s_gst = (gst / 2)
    c_gst = (gst / 2)
    
    if hotel.gst_status == 0:
        s_gst = 0
        c_gst = 0
        gst = 0
        
    total_price = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))['total_amount__sum']
    total_amount = math.floor(int(total_price) + int(gst))
    order_Master(
        table_id=table_id,
        total_price=total_price,
        order_filter=order_filter,
        s_gst=s_gst,
        c_gst=c_gst,
        cash_amount=total_amount,
        hotel_id=hotel_id
    ).save()
    o = order_Master.objects.filter(hotel_id=hotel_id,order_filter=order_filter).first()
    for i in Item.objects.filter(status=1):
        if Hotel_cart.objects.filter(table_id=table_id, item_id=i.id):
            order_Detail(
                order_master_id=o.id,
                item_id=i.id,
                qty=Hotel_cart.objects.filter(table_id=table_id, item_id=i.id).aggregate(Sum('qty'))['qty__sum'],
                price=Hotel_cart.objects.filter(table_id=table_id, item_id=i.id).aggregate(Sum('price'))['price__sum'],
                total_price=Hotel_cart.objects.filter(table_id=table_id, item_id=i.id).aggregate(Sum('total_amount'))['total_amount__sum'],
                order_filter=order_filter,
                item_name=i.marathi_name,
            ).save()
    Hotel_cart.objects.filter(table_id=table_id).delete()
    
@csrf_exempt
def running_table(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        table = []
        runing_table = []
        
        
        
        for t in Table.objects.filter(status=1, hotel_id=hotel.id):
            status = 'no'        
            c = Hotel_cart.objects.filter(table_id=t.id).exists()
            if c:
                runing_table.append({'id':t.id,'name':t.name})
                status = 'yes'        
            table.append({'id':t.id,'name':t.name,'status':status})
        if 'chang_paid_status'in request.POST:
            bill_id = request.POST.get('bill_id')
            b = order_Master.objects.filter(id=bill_id).first()
            b.paid_status = 1
            b.save()
        if 'delete_cart'in request.POST:
            cart_id = request.POST.get('cart_id')
            c_cart = Customer_cart.objects.filter(id=cart_id).first()
            table_id = c_cart.table_id
            c_cart.delete()
            
            # c_cart = Customer_cart.objects.filter(table_id=cart_id).first()
            # if c_cart == None and Hotel_cart.objects.filter(table_id=table_id).first() == None:
            #     Table_QrCode.objects.filter(table_id=table_id).update(status=0)
                
            return redirect('running_table')
        if 'accept_order'in request.POST:
            cart_id = request.POST.get('cart_id')
            c_cart = Customer_cart.objects.filter(id=cart_id).first()
            Hotel_cart(
                hotel_id=hotel.id,
                table_id=c_cart.table.id,
                item_id=c_cart.item.id,
                price=c_cart.price,
                total_amount=c_cart.total_amount,
                qty=c_cart.qty,
                note=c_cart.note,
                session_id=c_cart.customer_session_id
            ).save()
            c_cart.delete()
            return redirect('running_table')
        context={
            'hotel':hotel,
            'table':table,
            'runing_table':runing_table,
            'unpaid_bills':order_Master.objects.filter(paid_status=0, hotel_id=hotel.id).order_by('-id')[0:10],
        }
        return render(request, 'hotel/running_table.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def table(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        t = Table.objects.filter(hotel_id=hotel.id)
        if 'add_table'in request.POST:
            name = request.POST.get('name')
            Table(
                hotel_id=hotel.id,
                name=name
            ).save()
            return redirect('table')
        context={
            'hotel':hotel,
            'table':t,
            'next_table_count':t.count()+1
        }
        return render(request, 'hotel/table.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def employee(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        if 'add_new_enmploee' in request.POST:
            name = request.POST.get('name')
            emobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            type = request.POST.get('type')
            if Employee.objects.filter(mobile=emobile).exists():
                return redirect('employee')
            else:
                Employee(
                    hotel_id=hotel.id,
                    name=name,
                    mobile=emobile,
                    pin=pin,
                    type=type
                ).save()
                return redirect('employee')
        if 'edit_enmploee' in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            emobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            type = request.POST.get('type')
            e = Employee.objects.filter(id=id).first()
            e.name = name
            e.mobile = emobile
            e.pin = pin
            e.type = type
            e.save()
            return redirect('employee')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Employee.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('employee')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Employee.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('employee')
        context={
            'hotel':hotel,
            'employee':Employee.objects.filter(hotel_id=hotel)
        }
        return render(request, 'hotel/employee.html', context)
    else:
        return redirect('login')
    
def compress_image(image):
    im = Image.open(image)
    im_io = io.BytesIO()
    im.save(im_io, 'WEBP', quality=50)
    return im_io
@csrf_exempt
def item_detail(request, id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        i = Item.objects.filter(id=id).first()
        item_image_and_youtube_url = Item_image_and_youtube_url.objects.filter(item_id=id).first()
        if 'active'in request.POST:
            i.status = 0
            i.save()
            return redirect('item_detail', id)
        if 'deactive'in request.POST:
            i.status = 1
            i.save()
            return redirect('item_detail', id)
        if 'gst_active'in request.POST:
            i.gst_status = 0
            i.save()
            return redirect('item_detail', id)
        if 'edit_url'in request.POST:
            url = request.POST.get('url')
            item_image_and_youtube_url.youtube_url = url
            item_image_and_youtube_url.save()
            return redirect('item_detail', id)
        if 'add_url'in request.POST:
            url = request.POST.get('url')
            print(url)
            if item_image_and_youtube_url == None:
                Item_image_and_youtube_url(
                    item_id=id,
                ).save()
                item_image_and_youtube_url = Item_image_and_youtube_url.objects.filter(item_id=id).first()
            item_image_and_youtube_url.youtube_url = url
            item_image_and_youtube_url.save()
            return redirect('item_detail', id)
        if 'add_image'in request.POST:
            image = request.FILES.get('image')
            if image == None:
                pass
            else:
                if item_image_and_youtube_url == None:
                    Item_image_and_youtube_url(
                        item_id=id,
                    ).save()
                    item_image_and_youtube_url = Item_image_and_youtube_url.objects.filter(item_id=id).first()
                compressed_image = compress_image(image)
                item_image_and_youtube_url.image.save(image.name[:-5]+'.webp', compressed_image, save=True)
            return redirect('item_detail', id)
        if 'edit_image'in request.POST:
            image = request.FILES.get('image')
            if image:
                compressed_image = compress_image(image)
                item_image_and_youtube_url.image.save(image.name[:-5]+'.webp', compressed_image, save=True)
            return redirect('item_detail', id)
                
        if 'gst_deactive'in request.POST:
            i.gst_status = 1
            i.save()
            return redirect('item_detail', id)
        if 'edit_item_marathi_name' in request.POST:
            name = request.POST.get('marathi_name')
            i.marathi_name = name
            i.save()
            return redirect('item_detail', id=id)
        if 'edit_item_english_name' in request.POST:
            name = request.POST.get('english_name')
            i.english_name = name
            i.save()
            return redirect('item_detail', id=id)
        if 'edit_item_price' in request.POST:
            price = request.POST.get('price')
            i.price = price
            i.save()
            return redirect('item_detail', id=id)
        if 'select_item_category'in request.POST:
            c_id = request.POST.get('id')
            category_item = selected_item_category.objects.filter(category_id=c_id,item_id=i.id).first()
            if category_item:
                if category_item.status==0:
                    category_item.status = 1
                    category_item.save()
            else:
                selected_item_category(
                    category_id=c_id,
                    item_id=i.id,
                ).save()
            return redirect('item_detail', id=id)
        if 'unselect_category'in request.POST:
            c_id = request.POST.get('id')
            category_item = selected_item_category.objects.filter(category_id=c_id,item_id=i.id).first()
            if category_item:
                if category_item.status==1:
                    category_item.status = 0
                    category_item.save()
            return redirect('item_detail', id=id)
        category=[]
        for c in Category.objects.filter(status=1, hotel_id=hotel.id):
            if selected_item_category.objects.filter(category_id=c.id,item_id=id, status=1).exists():
                category.append({'id': c.id,'name':c.name, 'selected_status': 1})
            else:
                category.append({'id': c.id,'name':c.name, 'selected_status': 0})
        context={
            'hotel':hotel,
            'item':i,
            'category':category,
            'item_image_and_youtube_url':item_image_and_youtube_url,
        }
        return render(request, 'hotel/item_detail.html', context)
    else:
        return redirect('login')
     
def item(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        if 'add_item'in request.POST:
            marathi_name = request.POST.get('marathi_name')
            english_name = request.POST.get('english_name')
            price = request.POST.get('price')
            Item(
                hotel_id=hotel.id,
                marathi_name=marathi_name,
                english_name=english_name,
                price=price
            ).save()
            return redirect('item')
        context={
            'hotel':hotel,
            'item':Item.objects.filter(hotel_id=hotel.id).order_by('marathi_name'),
        }
        return render(request, 'hotel/item.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def category(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        hotel = Hotel.objects.filter(mobile=mobile).first()
        if 'add_category'in request.POST:
            name = request.POST.get('category_name')
            Category(
                hotel_id=hotel.id,
                name=name
            ).save()
            return redirect('category')
        if 'save_order_by'in request.POST:
            id = request.POST.get('category_id')
            order_by = request.POST.get('order_by')
            Category.objects.filter(id=id).update(order_by=order_by)
            return redirect('category')
        if 'edit_category'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('category_name')
            Category(
                id=id,
                hotel_id=hotel.id,
                name=name
            ).save()
            return redirect('category')
        context={
            'hotel':hotel,
            'category':Category.objects.filter(hotel_id=hotel.id).order_by('-order_by'),
        }
        return render(request, 'hotel/category.html', context)
    else:
        return redirect('login')