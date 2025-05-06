from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('refund_and_cancellation_policy/', views.refund_and_cancellation_policy, name='refund_and_cancellation_policy'),
    path('payment-verify/', views.payment_verify, name='payment-verify'),

]