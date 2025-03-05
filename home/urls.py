from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact_us/', views.contact_us, name='contact_us'),
]