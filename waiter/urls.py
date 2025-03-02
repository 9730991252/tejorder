from django.urls import path
from . import views
urlpatterns = [
    path('waiter_home/', views.waiter_home, name='waiter_home'),
    path('order/<table_id>', views.order, name='order'),
]