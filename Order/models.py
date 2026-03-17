from django.db import models
from django.conf import settings
from catalog.models import ProductVariant


class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Pending')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    shipping_price = models.DecimalField(max_digits=6,decimal_places=2,default=50.00)
    shipping_address = models.TextField()
    shipping_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.user_name}"
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    variant = models.ForeignKey(ProductVariant,on_delete=models.SET_NULL,null=True)

    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.name if self.variant else 'Deleted Product'}"