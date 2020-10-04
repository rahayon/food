import socket
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from requests.api import request
from sslcommerz_python.payment import SSLCSession

from order.models import Cart, Order
from payment.forms import BillingForm
from payment.models import BillingAddress


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.info(request, f'Shipping Address is saved')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs.count()
    order_total = order_qs[0].get_totals()
    return render(request, 'payment/checkout.html', context={'form': form, 'order_items': order_items, 'order_total': order_total,'order_items_count': order_items_count, 'saved_address': saved_address})

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]

    if not saved_address.is_fully_filled():
        messages.info(request, "Please Complete Billing Address")
        return redirect('payment:checkout')

    
    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please Complete your profile Details")
        return redirect('home:home')


    store_id = 'rahay5e7c01054d7ed'
    store_pass = 'rahay5e7c01054d7ed@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

    status_url = request.build_absolute_uri(reverse('payment:complete'))
    
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()

    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')
    
    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address, address2=current_user.profile.address, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.postcode, country=saved_address.country)

    response_data = mypayment.init_payment()

    return redirect(response_data['GatewayPageURL'])



@csrf_exempt
def complete(request):
    if request.method =='POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        print(status)
        if status == 'VALID':
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']
            # card_type = payment_data['card_type']
            tran_date = payment_data['tran_date']
            messages.success(request, f'Your Payment is completed successfully. Page will be redirected')
            return HttpResponseRedirect(reverse('payment:purchased', kwargs={'tran_id': tran_id, 'val_id': val_id, 'tran_date': tran_date},))

        if status =='FAILED' :
            messages.warning(request, f'your payment is Failed. Please Try Again Later')
            return redirect('payment:checkout')
    return render(request, 'payment/complete.html', context={})



@login_required
def purchased(request, tran_id, val_id, tran_date):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderID = orderId
    order.paymentID = val_id
    order.payment_date = tran_date
    order.save()

    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return redirect('home:home')


@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context ={
            'orders': orders
        }
    except:
        messages.warning(request, f"you do not have an active order")
        return redirect('home:home')
    return render(request, 'payment/order.html', context)


def invoice(request, pk):
    """
    docstring
    """
    try:
        
        orders = Order.objects.filter(pk=pk,user=request.user, ordered=True)
        order_total = orders[0].get_totals()
        invoice_id = orders[0].orderID
        invoice_date = orders[0].payment_date
        order_created = orders[0].created
        context ={
            'orders': orders,
            'order_total': order_total,
            'invoice_id': invoice_id,
            'invoice_date': invoice_date,
            'order_created': order_created
        }
    except:
        messages.warning(request, f"you do not have an active order")
        return redirect('home:home')

    return render(request, "payment/invoice.html", context)


