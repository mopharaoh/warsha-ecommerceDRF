from django.db import models
from django.conf import settings
from Order.models import Order
class Payment(models.Model):

    PAYMENT_METHODS = (
        ('Credit Card','Credit Card'),
        ('Cash on Delivery', 'Cash on Delivery'),
    )

    PAYMENT_STATUS = (
        ('Pending','Pending'),
        ('Successful','Successful'),
        ('Failed','Failed'),
        ('Refunded', 'Refunded'),
    )

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)

    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHODS,default='Credit Card')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Pending')
    transaction_id = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} - {self.status}"