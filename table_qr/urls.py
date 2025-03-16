from django.urls import path
from . import views
urlpatterns = [
    path ('generate_table_qrcode/<int:id>/<bg>', views.generate_table_qrcode, name='generate_table_qrcode'),
    path ('generate_nameplate_qrcode/<int:id>', views.generate_nameplate_qrcode, name='generate_table_qrcode'),
    path ('<url>/', views.customer_order, name='customer_order'),
    path ('its_running_table/<url>', views.its_running_table, name='its_running_table'),
]