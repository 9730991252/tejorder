from django.urls import path
from . import views

urlpatterns = [
    path('chef_helper_home/', views.chef_helper_home, name='chef_helper_home'),
]