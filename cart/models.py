from django.db import models
from ecommerceDRF import settings
from catalog.models import ProductVariant, Brand
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal


class Coupon(models.Model):
    code = models.CharField(max_length=100,unique=True)
    percentage = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)])
    valid = models.BooleanField(default=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='coupons',null=True,blank=True)

    def __str__(self):
        return f"{self.code} ({self.percentage}%) - {self.brand.name if self.brand else 'Global'}"

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    @property
    def total_price(self):
        total = Decimal('0.00')
        discount = Decimal('0.00')
        for item in self.items.all():
            item_total = item.sub_total
            total += item_total

            if self.coupon and self.coupon.valid:
                if self.coupon.brand is None or self.coupon.brand == item.variant.product.brand:
                    item_discount = item_total*(Decimal(self.coupon.percentage)/Decimal(100))
                    discount +=item_discount
        return total - discount
        
class CartItem(models.Model):

    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def sub_total(self):
        return self.variant.price * self.quantity
    
    class Meta:
        unique_together = ['cart','variant']