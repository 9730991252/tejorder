from django.shortcuts import render, redirect
from .models import *
from sunil.models import *
from hotel.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def chef_helper_home(request):
    if request.session.has_key('chef_helper_mobile'):
        mobile = request.session['chef_helper_mobile']
        c = Employee.objects.filter(mobile=mobile).first()
        if 'Accept_item_table'in request.POST:
            table_id = request.POST.get('table_id')
            h = Hotel_cart.objects.filter(table_id=table_id, cook_status='Pendding')
            for h in h:
                hc = Hotel_cart.objects.filter(id=h.id).first()
                hc.cook_status = 'Accepted'
                hc.chef_id = c.id
                hc.save()
            return redirect('chef_helper_home')
        if 'Accept_item'in request.POST:
            item_id = request.POST.get('item_id')
            h = Hotel_cart.objects.filter(item_id=item_id, cook_status='Pendding')
            for h in h:
                hc = Hotel_cart.objects.filter(id=h.id).first()
                hc.cook_status = 'Accepted'
                hc.chef_id = c.id
                hc.save()
            return redirect('chef_helper_home')
        if 'Accept_item_one'in request.POST:
            id = request.POST.get('id')
            hc = Hotel_cart.objects.filter(id=id).first()
            hc.cook_status = 'Accepted'
            hc.chef_id = c.id
            hc.save()
            return redirect('chef_helper_home')
        if 'Delivere'in request.POST:
            item_id = request.POST.get('item_id')
            table_id = request.POST.get('table_id')
            hc = Hotel_cart.objects.filter(item_id=item_id,table_id=table_id, chef_id = c.id).first()
            if hc:
                hc.cook_status = 'Delivered'
                hc.save()
            return redirect('chef_helper_home')
        
        context={
            'c':c,
            'pending_item':Hotel_cart.objects.filter(cook_status='Pendding', hotel_id=c.hotel_id),
            'accepted_item':Hotel_cart.objects.filter(cook_status = 'Accepted', chef_id=c.id),
            'delivered_item': Hotel_cart.objects.filter(cook_status='Delivered', chef_id=c.id)
        }
        return render(request, 'chef_helper/chef_helper_home.html', context)
    else:
        return redirect('/login/')