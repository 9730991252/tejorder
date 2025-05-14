from django.urls import path
from . import views

urlpatterns = [
    path('', views.sunil_login, name='sunil_login'),
    path('sunil_home/', views.sunil_home, name='sunil_home'),
    path('payment/', views.payment, name='payment'),
    path('razorpay_settlements/', views.razorpay_settlements, name='razorpay_settlements'),
    path('hotel_payment_detail/<id>', views.hotel_payment_detail, name='sunil_home'),
    path('sunil_shope_detail/<id>', views.sunil_shope_detail, name='sunil_shope_detail'),
]