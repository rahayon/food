from os.path import exists
from urllib import request

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from home.models import Product
from order.models import Cart, Order


# Create your views here.
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated")
            return redirect('order:cart')

        else:
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added in your cart")
            return redirect('order:cart')
    else:
        order = Order(user=request.user)
        order.save()
        messages.info(request, "This item was added in your cart")
        return redirect('order:cart')

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts': carts, 
            'orders': order,
            'carts_item_count': carts.count()
        }
        return render(request, 'order/cart.html', context)
    else:
        messages.warning(request, 'you dont have any item in your cart')
        return redirect('home:home')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user,purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your cart")
            return redirect('order:cart')
        else:
            messages.info(request, "You dont't have an active order!")
            return redirect('home:home')
    else:
        messages.info(request, "you dont have an active order!")
        return redirect('home:home')

@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists:
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.title} quantity has been updated")
                return redirect('order:cart')
        else:
            messages.info(request, f"{item.title} is not in your cart")
            return redirect('home:home')
    
    else:
        messages.info(request, "you dont have an active order")
        return redirect('home:home')


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.title} has been updated")
                return redirect('order:cart')
            
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f'{item.title} item has been removed from cart' )
                return redirect('order:cart')
            
        else:
            messages.info(request, f"{item.title} is not in your cart")
            return redirect('home:home')

    else:
        messages.info(request, 'you dont have an active cart')
        return redirect('home:home')
