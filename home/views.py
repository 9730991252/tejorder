from django.shortcuts import redirect, render
from sunil.models import *
from hotel.models import *
# Create your views here.
def index(request):
    return render(request, 'home/index.html')

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
