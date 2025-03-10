from django.urls import path
from . import views
urlpatterns = [
    path('chang_category_status/', views.chang_category_status, name='chang_category_status'),
    path('select_item_category/', views.select_item_category, name='select_item_category'),
    path('select_category_item/', views.select_category_item, name='select_category_item'),
    path('chang_teble_status/', views.chang_teble_status, name='chang_teble_status'),
    path('chang_teble_name/', views.chang_teble_name, name='chang_teble_name'),
    path('add_item_to_hotel_cart/', views.add_item_to_hotel_cart, name='add_item_to_hotel_cart'),
    path('filter_items_by_category/', views.filter_items_by_category, name='filter_items_by_category'),
    path('search_hotel_item/', views.search_hotel_item, name='search_hotel_item'),
    path('add_item_to_hotel_cart_admin/', views.add_item_to_hotel_cart_admin, name='add_item_to_hotel_cart_admin'),
    path('chang_order_table_id/', views.chang_order_table_id, name='chang_order_table_id'),
    path('item_gst_status/', views.item_gst_status, name='item_gst_status'),
    path('item_discount_status/', views.item_discount_status, name='item_discount_status'),
    path('add_item_to_customer_cart/', views.add_item_to_customer_cart, name='add_item_to_customer_cart'),
    path('add_item_to_cart_edit/', views.add_item_to_cart_edit, name='add_item_to_cart_edit'),
    path('filter_items_by_category_customer/', views.filter_items_by_category_customer, name='filter_items_by_category_customer'),
]