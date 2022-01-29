from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from partytree import upload
from . import views
from .import supervisor
from .import cashier


app_name = 'partytree'

urlpatterns = [
    path('manage_category/', supervisor.manage_category, name='manage_category'),
    path('create_category/', supervisor.create_category, name='create_category'),
    path('edit_category/<str:pk>/', supervisor.edit_category, name='edit_category'),
    path('manage_product/', supervisor.manage_product, name='manage_product'),
    path('create_product/', supervisor.create_product, name='create_product'),
    path('edit_product/<str:pk>/', supervisor.edit_product, name='edit_product'),

    path('create_restock/', supervisor.create_restock, name='create_restock'),
    path('manage_restock/', supervisor.manage_restock, name='manage_restock'),

    path('create_damage/', supervisor.create_damage, name='create_damage'),
    path('manage_damages/', supervisor.manage_damages, name='manage_damages'),

    path('manage_inventory/', supervisor.manage_inventory, name='manage_inventory'),
    path('EditInventory/<str:pk>/', supervisor.EditInventory, name='EditInventory'),

    path('create_order/', cashier.create_order, name='create_order'),
    path('orderitemss/<str:pk>/', cashier.orderitemss, name='orderitemss'),
    path('add_items_to_chart/<str:pk>/<str:order_id>/', cashier.add_items_to_chart,name='add_items_to_chart'),
    path('adjuest_quantity/<str:pk>/<str:order_id>/',cashier.adjuest_quantity,name='adjuest_quantity'),
    path('delete_item/<str:pk>/', cashier.deletes, name='delete_item'),
    path('cancel_order/<str:pk>/', cashier.cancel_order,name='cancel_order'),
    path('checkout/<str:pk>/', cashier.checkout, name='checkout'),
    path('search_order', cashier.search_order,name='search_order'),

    path('checkout_print/<str:pk>/', cashier.checkout_print, name='checkout_print'),
    path('Vew_order/<str:pk>/', cashier.Vew_order, name='Vew_order'),
    path('close_order', cashier.close_order, name='close_order'),
    path('close', cashier.close, name='close'),
    path('manage_order', cashier.manage_order, name='manage_order'),


    path('makepayment/<str:pk>/', cashier.makepayment, name='makepayment'),

    path('closing_stock/', supervisor.closing_stock, name='closing_stock'),
    path('closed_stock/', supervisor.closed_stock, name='closed_stock'),

    path('uploads_products', upload.uploads_products,name='uploads_products'),
    path('restock_products', upload.restock_products,name='restock_products'),
    path('daily_sales', cashier.daily_sales,name='daily_sales'),

]
