import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from myshop import settings
from orders.models import Order
from payment.tasks import payment_completed


@csrf_exempt
def stripe_webhooks(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:  # недопустимый payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:  # поддельная подпись
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':  # режим одноразовый платеж, статус оплаченно
            order = get_object_or_404(Order, id=session.client_reference_id)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            payment_completed.delay(order.id)
    return HttpResponse(status=200)
