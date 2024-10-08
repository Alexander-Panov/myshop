from django.urls import path

from payment import views
from payment.application import webhooks
from django.utils.translation import gettext_lazy as _

app_name = 'payment'

urlpatterns = [
    path(_('process/'), views.payment_process, name='process'),
    path(_('completed/'), views.payment_completed, name='completed'),
    path(_('cancelled/'), views.payment_canceled, name='canceled'),
]