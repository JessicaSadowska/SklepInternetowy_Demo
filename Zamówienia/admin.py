from django.contrib import admin
from Zamówienia.models import *


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'quantity', 'product_price', 'is_ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'email', 'imie_i_nazwisko', 'phone', 'order_total', 'is_ordered', 'created_at', 'updated_at']
    list_filter = ['order_number']
    search_fields = ['order_number', 'last_name', 'email']
    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
