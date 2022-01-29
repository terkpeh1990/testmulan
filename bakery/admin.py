from django.contrib import admin
from .models import *
# Register your models here.

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id','instock','outgoing','avialable_stock','avialable_stock_cost')
    search_fields = ['product_id__name']
    ordering = ['-id']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date','customer','gross_price','total_price','amount_paid','balance')
    search_fields = ['id','customer__name']
    ordering = ['-id']

admin.site.register(Inventory,InventoryAdmin)
admin.site.register(Inventory_records)
admin.site.register(Product)
admin.site.register(Order,OrderAdmin)
admin.site.register(Order_Details)
admin.site.register(Closing_stocks)