from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from . models import *
from hotel.models import *
from django.contrib import messages 
from django.db.models import Avg, Sum, Min, Max

# Create your views here.
def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["number"])
        b =int(request.POST["pin"])
        s = a+b
        su = Sunil.objects.filter().first()
        if s == int(su.sum) :
            request.session['sunil_mobile'] = s
            return redirect('/sunil/payment/')
        else:
            return redirect('sunil_login')
    return render(request, 'sunil/sunil_login.html')

def sunil_home(request):
    if request.session.has_key('sunil_mobile'):
        if 'Add_hotel'in request.POST:
            hotel_name = request.POST.get('hotel_name')
            owner_name = request.POST.get('owner_name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            if Hotel.objects.filter(mobile=mobile).exists():
                pass
            else:
                Hotel(
                    hotel_name=hotel_name,
                    owner_name=owner_name,
                    mobile=mobile,
                    pin=pin,
                ).save()    
            return redirect('sunil_home')
        if 'Edit_hotel'in request.POST:
            id = request.POST.get('id')
            hotel_name = request.POST.get('hotel_name')
            owner_name = request.POST.get('owner_name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            Hotel(
                id=id,
                hotel_name=hotel_name,
                owner_name=owner_name,
                mobile=mobile,
                pin=pin,
            ).save()
            return redirect('sunil_home')
        if 'login'in request.POST:
            id = request.POST.get('id')
            request.session['owner_mobile'] = Hotel.objects.filter(id=id).first().mobile
            return redirect('hotel_home')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Hotel.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('payment')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Hotel.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('payment')
        context={
            'hotel':Hotel.objects.all()
        }
        return render(request, 'sunil/sunil_home.html', context)
    else:
        return redirect('sunil_login')
    

def payment(request):
    if request.session.has_key('sunil_mobile'):
        h = []
        for i in Hotel.objects.filter(status=1):
            p = Hotel_Payment.objects.filter(hotel_id=i.id).order_by('-id')
            total_amount = p.aggregate(Sum('amount'))['amount__sum']
            total_bills = p.aggregate(Sum('bills'))['bills__sum']
            if total_amount == None:
                total_amount = 0
                total_bills = 0
            bill = order_Master.objects.filter(hotel_id=i.id).count()
            remaining_bills = (int(total_bills) - int(bill))
            h.append({
                'id':i.id,
                'hotel_name':i.hotel_name,
                'owner_name':i.owner_name,
                'address':i.address,
                'upi_id':i.upi_id,
                'logo':i.logo,
                'mobile':i.mobile,
                'pin':i.pin,
                'status':i.status,
                'gst_status':i.gst_status,
                'gst_number':i.gst_number,
                'discount_status':i.discount_status,
                'date':i.date,
                'total_amount':total_amount,
                'remaining_bills':remaining_bills,
            })
        context={
            'hotel':h,
        }
        return render(request, 'sunil/payment.html', context)
    else:
        return redirect('sunil_login')

@csrf_exempt    
def hotel_payment_detail(request,id):
    if request.session.has_key('sunil_mobile'):
        h = Hotel.objects.filter(id = id).first()
        if h:
            p = Hotel_Payment.objects.filter(hotel_id=h.id).order_by('-id')
            total_amount = p.aggregate(Sum('amount'))['amount__sum']
            total_bills = p.aggregate(Sum('bills'))['bills__sum']
            if total_amount == None:
                total_amount = 0
                total_bills = 0
            bill = order_Master.objects.filter(hotel_id=h.id).count()
            remaining_bills = (int(total_bills) - int(bill))
            if 'add_hotel_payment'in request.POST:
                amount = request.POST.get('amount')
                bills = request.POST.get('bills')
                type = request.POST.get('type')
                mobile = request.POST.get('mobile')
                date = request.POST.get('date')
                add_hotel_payment(h, amount, bills, type, mobile, date)
                return redirect(f'/sunil/hotel_payment_detail/{id}')
            if 'edit_hotel_payment'in request.POST:
                p_id = request.POST.get('p_id')
                amount = request.POST.get('amount')
                bills = request.POST.get('bills')
                type = request.POST.get('type')
                mobile = request.POST.get('mobile')
                date = request.POST.get('date')
                Hotel_Payment.objects.filter(id=p_id).update(
                    amount=amount,
                    bills=bills,
                    type=type,
                    mobile=mobile,
                    date=date
                )
                return redirect(f'/sunil/hotel_payment_detail/{id}')
        context={
            'hotel':h,
            'payments':p,
            'total_amount':total_amount,
            'total_bills':total_bills,
            'remaining_bills':remaining_bills
        }
        return render(request, 'sunil/hotel_payment_detail.html', context)
    else:
        return redirect('sunil_login')

def add_hotel_payment(hotel,amount,bills,type, mobile,date):
    Hotel_Payment(
        hotel_id=hotel.id,
        amount=amount,
        bills=bills,
        type=type,
        mobile=mobile,
        date=date,
    ).save()

@csrf_exempt
def sunil_shope_detail(request, id):
    if request.session.has_key('sunil_mobile'):
        h = Hotel.objects.filter(id = id).first()
        items = Item.objects.filter(hotel_id=h.id)
        if 'mobile'in request.POST:
            mobile = request.POST.get('mobile_i')
            ht = Hotel.objects.filter(mobile=mobile).first()
            if ht:
                if ht.id == h.id: 
                    h.mobile = mobile
                    h.save()
                else:
                    messages.warning(request,"Mobile Number Already Exist")
            else:
                h.mobile = mobile
                h.save()
            return redirect('sunil_shope_detail', id)
        
        if 'active'in request.POST:
            h.status = 0
            h.save()
            return redirect('sunil_shope_detail', id)
        if 'deactive'in request.POST:
            h.status = 1
            h.save()
            return redirect('sunil_shope_detail', id)
        
        if 'gst_active'in request.POST:
            items.update(gst_status=0)
            h.gst_status = 0
            h.discount_status = 1
            h.save()
            return redirect('sunil_shope_detail', id)
        if 'gst_deactive'in request.POST:
            h.gst_status = 1
            items.update(discount_status=0)
            h.discount_status = 0
            h.save()
            return redirect('sunil_shope_detail', id)
        
        if 'discount_active'in request.POST:
            items.update(discount_status=0)
            h.discount_status = 0
            h.save()
            return redirect('sunil_shope_detail', id)
        if 'discount_deactive'in request.POST:
            if h.gst_status == 0:
                h.discount_status = 1
                h.save()
            return redirect('sunil_shope_detail', id)
        context={
            'hotel':h
        }
        return render(request, 'sunil/sunil_shope_detail.html', context)
    else:
        return redirect('sunil_login')