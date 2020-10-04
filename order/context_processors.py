from order.models import Cart, Order
from django.contrib.auth.decorators import login_required

@login_required
def cart_info(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    
    if carts.exists() and orders.exists():
        order = orders[0]

        return {
            'carts': carts, 
            'order': order,
            'item_count': carts.count()
        }
    