import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from cart.cart import Cart
from myshop import settings
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from orders.tasks import order_created


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # запусить асинхронную задачу
            order_created.delay(order.id)
            # Задать заказ в сеансе
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})

    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html',
                  {'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT / 'css/pdf.css'
                                           )])
    return response
