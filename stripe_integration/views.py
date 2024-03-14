
import json
import stripe
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import dotenv_values
from .models import Order, Product

stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

@csrf_exempt
def create_checkout_session(request, product_id):
     #Updated- creating Order object
    product = Product.objects.get(id=product_id)
    order=Order(product = product, email=" ",paid="False",amount=0,description=" ")
    order.save()
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
        'currency': 'inr',
        'product_data': {
                        'name': product.name,
                        "description":f'{product.description} and image urls is : https://3917-103-97-240-96.ngrok-free.app{product.image.url}',
                        "images": [f'https://3917-103-97-240-96.ngrok-free.app{product.image.url}'],
                        },
                    'unit_amount': int(product.price)*100,
                    },
        'quantity': 1,
        }],
    metadata={
        "order_id": order.id,
        },
    mode='payment',
    success_url=YOUR_DOMAIN + '/stripe/success',
    cancel_url=YOUR_DOMAIN + '/stripe/cancel',
    )
    return JsonResponse({'id': session.id})

#home view
def home(request):
    env_vars = dotenv_values('.env')
    context = {"stripe_publishable_key" : settings.STRIPE_PUBLISHABLE_KEY, 'products': Product.objects.all()}

    return render(request,'stripe_integration/checkout.html', context)

#success view
def success(request):
    return render(request,'stripe_integration/success.html')

#cancel view
def cancel(request):
    return render(request,'stripe_integration/cancel.html')

@csrf_exempt
def webhook(request):
    print("webhook called    "*50)
    endpoint_secret = settings.STRIPE_WEBHOOK_SIGNING_KEY
    print("endpoint secret", endpoint_secret)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print("request.body",request.body)
    print("request.Meta",request.META)
    print("request.headers",request.headers)
    print("request",request)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    
    print("event['type']",event['type'])

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_details']['email']
        price = session["amount_total"] /100
        sessionID = session["id"]
        #grabbing id of the order created
        ID=session["metadata"]["order_id"]
        print("ID",ID)
        print('session["metadata"]',session["metadata"])
        #Updating order
        Order.objects.filter(id=ID).update(email=customer_email,amount=price,paid=True,description=sessionID)
    else:
      print('Unhandled event type {}'.format(event['type']))
    return HttpResponse({"message":"payment Done successfully"}, status=200)
