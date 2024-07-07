from django.contrib import admin
from .models import *
# Register your models here.



class OrderDetailInline(admin.TabularInline):
    model = GrandOrder.orders.through
    extra = 1
    fields = ('fooditem', 'quantity', 'total_price')
    readonly_fields = ('fooditem', 'quantity', 'total_price')
    verbose_name = "Order Detail"
    verbose_name_plural = "Order Details"

    def fooditem(self, obj):
        return obj.orderdetail.fooditem.name
    
    def quantity(self, obj):
        return obj.orderdetail.quantity
    
    def total_price(self, obj):
        return obj.orderdetail.total_price

    fooditem.short_description = 'Food Item'
    quantity.short_description = 'Quantity'
    total_price.short_description = 'Total Price'

class GrandOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'grand_total', 'phone_number', 'item_names', 'item_quantities')
    inlines = [OrderDetailInline]
    search_fields = ('id',)
    def item_names(self, obj):
        return ", ".join([str(order.fooditem.name) for order in obj.orders.all()])
    
    def item_quantities(self, obj):
        return ", ".join([str(order.quantity) for order in obj.orders.all()])
    
    item_names.short_description = 'Item Names'
    item_quantities.short_description = 'Item Quantities'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(GrandOrderAdmin, self).get_inline_instances(request, obj)

admin.site.register(FoodType)
admin.site.register(FoodItem)
admin.site.register(GrandOrder, GrandOrderAdmin)
admin.site.register(orderDetail)

