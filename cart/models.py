from django.db import models
from ecommerceDRF import settings
from catalog.models import ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.sub_total for item in self.items.all())

class CartItem(models.Model):

    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def sub_total(self):
        return self.variant.price * self.quantity