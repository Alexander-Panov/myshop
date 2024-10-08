from django import forms

from orders.models import Order
from localflavor.ru.forms import RUPostalCodeField


class OrderCreateForm(forms.ModelForm):
    postal_code = RUPostalCodeField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']