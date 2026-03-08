from django.db import models
# from django.contrib.auth.models import User
from ecommerceDRF.settings import AUTH_USER_MODEL as User


def upload_to(instance, filename):
    product_id = instance.variant.product.id if instance.variant.product else 'temp'
    return f'products/{product_id}/{filename}'
class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100,unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,unique=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):

    name  =models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='products')
    is_bundle = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    matarial = models.CharField(null=True,blank=True,max_length=25)
    style = models.CharField(max_length=50, null=True, blank=True)
    dimensions = models.CharField(max_length=90, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.product.name} - { 'variant'}"

class ProductImage(models.Model):

        variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name='images')
        image = models.ImageField(upload_to=upload_to,default="default.jpg")

        def __str__(self):
            return f"{self.variant.product}-{self.variant}"