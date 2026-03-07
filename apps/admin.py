from django.contrib import admin

from apps.models.user import Users
from apps.models.order import Order, OrderItem
from apps.models.product import (
    Category, Product, ProductImage, Tags,
    Size, Color, ShoppingCart
)


admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Tags)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Users)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'id']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'id']


class OrderItemStackedInline(admin.StackedInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'is_status', 'total_order_price', 'created_at', 'id']
    inlines = [OrderItemStackedInline, ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'count', 'id']

