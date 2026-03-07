from django.urls import path

from apps.views import (
    ProductListView, ProductDetailView, ShoppingCartList,
    UserLoginView, UserRegisterView, add_to_cart, user_logout,
    remove_to_cart, OrderListView, OrderDetailView, 
    CheckOutView, order_create, order_update, 
    OperatorView, UserProfileView, order_update_w_operator
)


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('shopping-cart/', ShoppingCartList.as_view(), name='shopping_cart'),
    path('shopping-cart-create/', add_to_cart, name='shopping_cart_create'),
    path('shopping-cart-remove/<int:pk>/', remove_to_cart, name='shopping_cart_remove'),

    # order
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-create/', order_create, name='order_create'),
    path('order-update/<int:pk>/', order_update, name='order_update'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),

    # operator
    path('operator-list/', OperatorView.as_view(), name='operator_list'),
    path('order-update-w-operator/<int:pk>/', order_update_w_operator, name='order_update_w_operator'),

    # auth
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile')
]


