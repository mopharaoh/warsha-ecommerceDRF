from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from Order.models import Order
from .models import Payment
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from .tasks import webhook_task
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,sig_header,endpoint_secret
        )
    except ValueError as e :
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata',{}).get('order_id')
        if order_id:
            webhook_task.delay(order_id)
    
    return HttpResponse(status=200)


class CreateStripeCheckout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,order_id):

        order = get_object_or_404(Order,id=order_id,user=request.user)
        if order.status != 'Pending':
            return Response(
                {"error": "This order cannot be paid for (it may already be paid or cancelled)."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            amount_in_cents = int(order.total_amount * 100)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'], 
                line_items=[
                    {
                        'price_data': {
                            'currency': 'egp', 
                            'unit_amount': amount_in_cents,
                            'product_data': {
                                'name': f'Order #{order.id}',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
               
                success_url= request.build_absolute_uri('/payment/success/'),
                cancel_url= request.build_absolute_uri('/payment/cancel/'),
                
                metadata={
                    'order_id': order.id
                }
            )
            payment, created = Payment.objects.update_or_create(
                order=order,
                defaults={
                    'user': request.user,
                    'amount': order.total_amount,
                    'status': 'Pending',
                    'transaction_id': checkout_session.id
                }
            )

            return Response({
                'checkout_url': checkout_session.url
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)