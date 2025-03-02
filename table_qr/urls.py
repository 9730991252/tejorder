from django.urls import path
from . import views
urlpatterns = [
    path ('generate_table_qrcode/<int:id>', views.generate_table_qrcode, name='generate_table_qrcode'),
    path ('<url>/', views.customer_order, name='customer_order'),
]