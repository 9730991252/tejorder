from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from table_qr.models import *
from sunil.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Sum, Min, Max
import math
from datetime import date
from PIL import Image
import io
from datetime import datetime, date, time, timedelta
from django.core.paginator import Paginator
from django.contrib import messages 
from django.utils.decorators import method_decorator
import razorpay
from django.conf import settings
from django.http import JsonResponse
from requests.auth import HTTPBasicAuth

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def handling_404(request, exception):
    return render(request, '404.html')

def index(request):
    
        
    visitors = Visitors.objects.all().first()
    if Visitors.objects.all().exists():
        visitors.count += 1
        visitors.save()
    else:
        Visitors().save()
    visitors = Visitors.objects.all().first()
    users = (int(Employee.objects.all().count()) + int(Hotel.objects.all().count()) + 150)
    
    bills = (int(order_Master.objects.all().count()) + int(290815))
    
    context = {
        'visitors': visitors,
        'users':users,
        'bills':bills,
    }
    
    return render(request, 'home/index.html',context)

@csrf_exempt 
def payment_verify(request):
    if request.method == 'POST':
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        signature = request.POST.get('razorpay_signature')
        
        payment = Hotel_Payment.objects.all().last()
        if client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }):
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.is_paid = True
            payment.bills = payment.amount * 3
            payment.save()
        else:
            payment.is_paid = False
            payment.save()
        return redirect('software_charges')

def contact_us(request):
    return render(request, 'home/contact_us.html')

def terms_and_conditions(request):
    return render(request, 'home/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')

def refund_and_cancellation_policy(request):
    return render(request, 'home/refund_and_cancellation_policy.html')

def pricing(request):
    return render(request, 'home/pricing.html')

def login(request):
    if request.session.has_key('owner_mobile'):
         return redirect('hotel_home')
    if request.session.has_key('waiter_mobile'):
         return redirect('waiter_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            h= Hotel.objects.filter(mobile=number,pin=pin,status=1)
            e = Employee.objects.filter(mobile=number,pin=pin,status=1).first()
            if h:
                request.session['owner_mobile'] = request.POST["number"]
                return redirect('hotel_home')
            elif e:
                if e.type == 'waiter':
                    request.session['waiter_mobile'] = request.POST["number"]
                    return redirect('waiter_home')
                else:
                    request.session['chef_helper_mobile'] = request.POST["number"]
                    return redirect('chef_helper_home')
            else:
                return redirect('/login/')
    return render(request, 'home/login.html')

def logout(request):
    if request.session.has_key('owner_mobile'):
        del request.session['owner_mobile']
    if request.session.has_key('waiter_mobile'):
        del request.session['waiter_mobile']
    if request.session.has_key('chef_helper_mobile'):
        del request.session['chef_helper_mobile']
    return redirect('/')
