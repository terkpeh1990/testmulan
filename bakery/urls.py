from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .import supervisor
from .import cashier


app_name = 'shop'

urlpatterns = [
    path('manage_category/',supervisor.manage_category, name='manage_category'),
    path('create_category/',supervisor.create_category, name='create_category'),
    path('edit_category/<str:pk>/',supervisor.edit_category, name='edit_category'),
    path('manage_product/', supervisor.manage_product, name='manage_product'),
    path('create_product/',supervisor.create_product, name='create_product'),
    path('edit_product/<str:pk>/', supervisor.edit_product, name='edit_product'),

    path('create_restock/', supervisor.create_restock, name='create_restock'),
    path('approve_restock/<str:pk>/',supervisor.approve_restock, name='approve_restock'),
    path('cancel_restock/<str:pk>/', supervisor.cancel_restock, name='cancel_restock'),
    path('manage_restock/', supervisor.manage_restock, name='manage_restock'),

    path('create_damage/', supervisor.create_damage, name='create_damage'),
    path('cancel_damages/<str:pk>/',
         supervisor.cancel_damages, name='cancel_damages'),

    path('manage_damages/', supervisor.manage_damages, name='manage_damages'),
    path('approve_damage/<str:pk>/',
         supervisor.approve_damage, name='approve_damage'),

    path('manage_inventory/', supervisor.manage_inventory, name='manage_inventory'),
    path('EditInventory/<str:pk>/',supervisor.EditInventory, name='EditInventory'),

    path('create_customer/', cashier.create_customer, name='create_customer'),
    path('orderitems/', cashier.orderitems.as_view(), name='orderitems'),
    path('delete_item/<str:pk>/', cashier.deletes, name='delete_item'),
    path('checkout/', cashier.checkout, name='checkout'),
    path('checkout_print/<str:pk>/', cashier.checkout_print, name='checkout_print'),
    path('Vew_order/<str:pk>/', cashier.Vew_order, name='Vew_order'),
    path('close_order', cashier.close_order, name='close_order'),
    path('close', cashier.close, name='close'),
    path('manage_order', cashier.manage_order, name='manage_order'),

    path('Takeorderitems/', cashier.Takeorderitems.as_view(), name='Takeorderitems'),
    path('makepayment/<str:pk>/', cashier.makepayment, name='makepayment'),

    path('closing_stock/', supervisor.closing_stock, name='closing_stock'),
    path('closed_stock/', supervisor.closed_stock, name='closed_stock'),
    path('approve_closing_stock/<str:pk>/',
         supervisor.approve_closing_stock, name='approve_closing_stock'),

    path('pending_restock/', supervisor.pending_restock, name='pending_restock'),
    path('pending_damages/', supervisor.pending_damages, name='pending_damages'),
    path('pending_stock/', supervisor.pending_stock, name='pending_stock'),
    path('daily_sales/', supervisor.daily_sales, name='daily_sales'),
    path('debt/', cashier.debt, name='debt'),
    path('taxation/', supervisor.taxation, name='taxation'),
    path('run_to_zero',supervisor.run_to_zero,name='run_to_zero'),
    path('clear_restock',supervisor.clear_restock,name='clear_restock'),
    path('clear_damage',supervisor.clear_damage,name='clear_damage'),
    path('clear_closing',supervisor.clear_closing,name='clear_closing'),
    path('clear_order',supervisor.clear_order,name='clear_order'),


    path('manage_snack', supervisor.manage_snack,name='manage_snack'),
    path('create_snack',supervisor.create_snack,name='create_snack'),
    path('snack_detail',supervisor.snack_detail.as_view(),name='snack_detail'),
    path('View_snack/<str:pk>/',supervisor.View_snack,name='View_snack'),
    path('cancel_snack/<str:pk>/',supervisor.cancel_snack,name='cancel_snack'),
    path('approve_snack/<str:pk>/',supervisor.approve_snack,name='approve_snack'),
    path('pending_snack',supervisor.pending_snack,name='pending_snack'),
    path('deletes_snackitems/<str:pk>/',supervisor.deletes_snackitems,name='deletes_snackitems'),
    path('delete_snack/<str:pk>/',supervisor.delete_snack,name='delete_snack'),
    path('closesnack',supervisor.closesnack,name='closesnack'),
    path('snackorder/<str:pk>/',supervisor.snackorder,name='snackorder'),
    path('View_snacked/<str:pk>/',supervisor.View_snacked,name='View_snacked'),













]
