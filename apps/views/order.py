from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView

from apps.models.order import Order, OrderItem
from apps.models.product import ShoppingCart


class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order-list.html'
    login_url = 'login'


class OperatorView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/operators.html'
    context_object_name = 'order_list'
    login_url = 'login'
    # ordering = ['-id']


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order-details.html'
    context_object_name = 'order'


class CheckOutView(TemplateView):
    template_name = 'orders/checkout.html'


@login_required
def order_create(request):
    new_order = Order.objects.create(user_id=request.user.id)
    new_order.save()
    order_id = new_order.id
    order_item_list = request.user.my_carts
    for i in order_item_list.all():
        new_order_item = OrderItem.objects.create(
        order_id=order_id,
        count=1,
        product_id=i.product.id,
    )
        new_order_item.save()
        cart = ShoppingCart.objects.filter(id=i.id).first()
        cart.delete()

    # return redirect('checkout')
    return render(request, "orders/checkout.html", context={ "order": new_order })


def order_update(request, pk):
    if request.method == "POST":

        data = request.POST

        phone = data.get("phone_number")
        address = data.get("address")
        description = data.get("notes")
        payment_method = data.get("payment_method")

        db_order = Order.objects.filter(id=pk).first()

        if db_order:
            
            db_order.phone = phone
            db_order.address = address
            db_order.description = description
            db_order.payment_method = payment_method
            db_order.is_status = "confirmed"
            db_order.save()

    return redirect("order_list")


def order_update_w_operator(request, pk):

    new_status = request.GET.get('status')

    db_order = Order.objects.filter(id=pk).first()

    if db_order:
        db_order.is_status = new_status
        db_order.save()

    return redirect("operator_list")

