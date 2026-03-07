from django.db import models
from django.core.validators import MinValueValidator

from apps.models.base import BaseCreatedModel
from apps.models.user import Users
from apps.models.product import Product, Color, Size



class Order(BaseCreatedModel):
    class OrderStatusChoice(models.TextChoices):
        PENDING = 'pending', 'Kutilmoqda'          # Buyurtma tushdi, lekin hali ko'rilmadi
        CONFIRMED = 'confirmed', 'Tasdiqlandi'     # Admin buyurtmani ko'rib, tasdiqladi
        PROCESSING = 'processing', 'Tayyorlanmoqda' # Omborxonada qadoqlanmoqda
        SHIPPED = 'shipped', 'Yo‘lga chiqdi'       # Kuryerga berildi yoki pochta yo'lida
        DELIVERED = 'delivered', 'Yetkazildi'      # Mijoz mahsulotni qabul qilib oldi
        CANCELLED = 'cancelled', 'Bekor qilindi'   # Mijoz yoki admin tomonidan bekor qilindi
        RETURNED = 'returned', 'Qaytarildi'

    class PaymentMethodChoice(models.TextChoices):
        CASH = 'cash', 'Naqd pul'
        CARD = 'card', 'Plastik karta (Terminal)'
        CLICK = 'click', 'Click'
        PAYME = 'payme', 'Payme'
        UZUM = 'uzum', 'Uzum Bank'

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(verbose_name="Zakar borishi kk bo'lgan manzil", blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_status = models.CharField(
        max_length=30,
        choices=OrderStatusChoice.choices,
        default=OrderStatusChoice.PENDING
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoice.choices,
        default=PaymentMethodChoice.CASH,
        verbose_name="To'lov usuli"
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_order_price(self):
        return sum(item.item_total_price for item in self.items.all())
    
    
    
    def __str__(self):
        return self.user.username


class OrderItem(BaseCreatedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.BigIntegerField(help_text="Sotib olingan vaqtdagi narxi", editable=False) 
    count = models.IntegerField(validators=[MinValueValidator(1)])
    
    selected_color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    selected_size  = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def item_total_price(self):
        return self.price * self.count
    
    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        self.price = self.product.price
        return super().save(*args, **kwargs)
    