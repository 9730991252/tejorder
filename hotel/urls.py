from django.urls import path
from . import views
urlpatterns = [
    path('hotel_home/', views.hotel_home, name='hotel_home'),
    path('item/', views.item, name='item'),
    path('item_detail/<id>', views.item_detail, name='item_detail'),
    path('category/', views.category, name='category'),
    path('employee/', views.employee, name='employee'),
    path('table/', views.table, name='table'),
    path('profile/', views.profile, name='profile'),
    path('running_table/', views.running_table, name='running_table'),
    path('view_order/<int:table_id>', views.view_order, name='view_order'),
    path('complate_view_order/<int:order_filter>', views.complate_view_order, name='complate_view_order'),
    path('complate_order/', views.complate_order, name='complate_order'),
    path('table_qr/', views.table_qr, name='table_qr'),
    path('report/', views.report, name='report'),
    path('software_charges/', views.software_charges, name='software_charges'),
    path('edit_pin/', views.edit_pin, name='edit_pin'),
    path('edit_bill/<id>', views.edit_bill, name='edit_bill'),
    path('print_completed_bill/<order_filter>/<qr_status>', views.print_completed_bill, name='report'),
]