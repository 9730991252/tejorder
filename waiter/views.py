from django.shortcuts import render, redirect
from .models import *
from sunil.models import *
from hotel.models import *
from table_qr.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def waiter_home(request):
    if request.session.has_key('waiter_mobile'):
        mobile = request.session['waiter_mobile']
        w = Employee.objects.filter(mobile=mobile).first()
        table = []
        runing_table = []
        for t in Table.objects.filter(status=1, hotel_id=w.hotel_id):
            status = 'no'        
            c = Hotel_cart.objects.filter(table_id=t.id).exists()
            if c:
                runing_table.append({'id':t.id,'name':t.name})
                status = 'yes'        
            table.append({'id':t.id,'name':t.name,'status':status})
        if 'delete_cart'in request.POST:
            cart_id = request.POST.get('cart_id')
            c_cart = Customer_cart.objects.filter(id=cart_id).first()
            table_id = c_cart.table_id
            c_cart.delete()
            return redirect('waiter_home')
        if 'accept_order'in request.POST:
            cart_id = request.POST.get('cart_id')
            c_cart = Customer_cart.objects.filter(id=cart_id).first()
            Hotel_cart(
                hotel_id=w.hotel.id,
                table_id=c_cart.table.id,
                item_id=c_cart.item.id,
                price=c_cart.price,
                total_amount=c_cart.total_amount,
                qty=c_cart.qty,
                note=c_cart.note,
                session_id=c_cart.customer_session_id,
                employee_id = w.id
            ).save()
            c_cart.delete()
            return redirect('waiter_home')
        context={
            'w':w,
            'table':table,
            'runing_table':runing_table
        }
        return render(request, 'waiter/waiter_home.html', context)
    else:
        return redirect('/login/')
    
@csrf_exempt
def order(request,table_id):
    if request.session.has_key('waiter_mobile'):
        mobile = request.session['waiter_mobile']
        w = Employee.objects.filter(mobile=mobile).first()
        if 'Delete'in request.POST:
            cart_id = request.POST.get('cart_id')
            Hotel_cart.objects.filter(id=cart_id).delete()
            return redirect(f'/waiter/order/{table_id}') 
        context={
            'w':w,
            'table':Table.objects.get(id=table_id),
            'category':Category.objects.filter(status=1),
            'cart':Hotel_cart.objects.filter(table_id=table_id),
            'table_id':table_id

        }
        return render(request, 'waiter/order.html', context)
    else:
        return redirect('login')