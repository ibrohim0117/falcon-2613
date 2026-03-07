from django.shortcuts import redirect
from django.views.generic import (
    ListView, TemplateView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from apps.models.product import Product, ShoppingCart



class ProductListView(ListView):
    model = Product
    template_name = 'product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        data = super().get_queryset()
        q_name = self.request.GET.get('q')
        if q_name:
            data = Product.objects.filter(name__contains=q_name).all()
        return data
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-details.html'
    context_object_name = 'product'
    slug_field = "slug"
    


class ShoppingCartList(LoginRequiredMixin, TemplateView):
    template_name = 'product/shopping-cart.html'
    login_url = 'login'


@login_required(login_url='login')
def add_to_cart(request):
    
    if request.method == "POST":
        data = request.POST
        product_id = data.get('product')
        user_id = request.user.id
        new_cart = ShoppingCart.objects.create(
            product_id=product_id,
            user_id=user_id
        )
        new_cart.save()
        
        return redirect('shopping_cart')


@login_required(login_url='login')
def remove_to_cart(request, pk):
    product_id = pk
    user_id = request.user.id
    db_card = ShoppingCart.objects.filter(id=product_id, user_id=user_id)
    if db_card.exists():
        db_card.delete()
        return redirect('shopping_cart')
    return redirect('shopping_cart')

