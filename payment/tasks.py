from celery import shared_task
from django.conf import settings
from .models import Payment
from Order.models import Order
from django.core.mail import send_mail

@shared_task
def webhook_task(order_id):
    try:
        payment = Payment.objects.get(order__id=order_id)
        payment.status = 'Successful'
        payment.save()
                
        order=Order.objects.get(id=order_id)
        order.status = 'Processing'
        
        order.save()

        subject = f"Order #{order.id} Confirmed - Warsha"               
        message = f"""
        Hello {order.user.user_name},
        
        Thank you for your purchase!
        We have successfully received your payment of {payment.amount} EGP.
       Your order is now being processed and will be shipped to:
       {order.shipping_address}
                
       Order Details:
        Status: {order.status}
        Order ID: {order.id} 
                
        Thanks for shopping with us!
        """
        send_mail(subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[order.user.email],
                    fail_silently=False)
        return f"Payment successful and Email sent for Order {order_id}"
                
    except (Payment.DoesNotExist, Order.DoesNotExist):
                return f"Error: Order or Payment not found for Order ID {order_id}"
                                