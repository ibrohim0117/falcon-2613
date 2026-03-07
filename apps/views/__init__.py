from .order import (
    OrderListView, OperatorView,
    OrderDetailView, CheckOutView, order_create,
    order_update, order_update_w_operator
)

from .product import(
     ProductDetailView, ProductListView, remove_to_cart,
    add_to_cart, ShoppingCartList
)

from .user import (
    UserLoginView, UserProfileView,
    UserRegisterView, user_logout
)