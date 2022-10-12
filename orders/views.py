from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
import razorpay

from cart.models import Cartitem, Coupon, UsedCoupons
from cart.views import UsedCoupon
from .forms import OrderForm
from product.models import product
from django.http import HttpResponse, JsonResponse
# Create your views here.
from .models import Order, OrderProduct
from .models import Payment
import datetime
import json


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    print(body)
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status='Order Placed'
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_item = Cartitem.objects.filter(user=request.user)
    for item in cart_item:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.products_id
        orderproduct.quantity = item.quantity
        if item.products.Offer_Price():
            offer_price = product.Offer_Price(item.products)
            price = offer_price["new_price"]
            orderproduct.product_price = price
        else:
            orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        cart_item = Cartitem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        products = product.objects.get(id=item.products.id)
        products.stock -= item.quantity
        products.save()

    Cartitem.objects.filter(user=request.user).delete()
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request, total=0, quntity=0):
    current_user = request.user
    cart_items = Cartitem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('storepage')
    granttotal = 0
    tax = 0
    if 'coupon_code' in request.session:
        print(request.session['coupon_code'])

        coupon = Coupon.objects.get(coupon_code=request.session['coupon_code'])
        reduction = coupon.amount
        print(reduction)

    else:
        reduction = 0
    for cart_item in cart_items:
        if cart_item.products.Offer_Price():
            offer_price = product.Offer_Price(cart_item.products)
            print(offer_price["new_price"])
            total = total + (
                    offer_price["new_price"] * cart_item.quantity
            )
            print(total)
        else:
            total = total + (cart_item.products.price * cart_item.quantity)

        quntity = quntity + cart_item.quantity
    tax = (18 * total) / 100
    a = total + tax

    granttotal = round(a, 2) - reduction

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()

            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = granttotal
            data.tax = tax
            data.reduction = reduction
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number

            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_item': cart_items,
                'total': total,
                'tax': tax,
                'granttotal': granttotal
            }
            print(cart_items)
            request.session['orderid'] = order_number

            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print('trancid in order complett',transID)
    if 'coupon_code' in request.session:
        print(request.session['coupon_code'])
        coupon = Coupon.objects.get(coupon_code=request.session['coupon_code'])
        del request.session['coupon_code']
        reduction = coupon.amount
        print(reduction)
        data = UsedCoupons(user=request.user, coupon=coupon)
        data.save()



    else:
        reduction = 0

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        ordered_products.reduction = reduction
        ordered_products.update()

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        subtotal - reduction

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'discount': reduction
        }

        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def cod(request):
    current_user = request.user
    orderid = request.session["orderid"]

    order = Order.objects.get(user=current_user, is_ordered=False, order_number=orderid)
    print(order)

    # save payment informations
    payment = Payment(
        user=current_user,
        payment_id=orderid,
        payment_method="Cash On Delivery",
        amount_paid=order.order_total,
        status="Completed",
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_item = Cartitem.objects.filter(user=request.user)
    for item in cart_item:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.products_id
        orderproduct.quantity = item.quantity
        if item.products.Offer_Price():
            offer_price = product.Offer_Price(item.products)
            price = offer_price["new_price"]
            orderproduct.product_price = price
        else:
            orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        cart_item = Cartitem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        products = product.objects.get(id=item.products.id)
        products.stock -= item.quantity
        products.save()

    Cartitem.objects.filter(user=request.user).delete()

    # for review coupons and reduce count

    # send transaction successfull
    param = (
            "order_number="
            + order.order_number
            + "&payment_id="
            + payment.payment_id
    )
    ################
    # capture the payemt
    messages.success(request, "Payment Success")
    print('orderid in cod',orderid)
    if "order_number" in request.session:
        del request.session["orderid"]

    redirect_url = reverse("order_complete")
    return redirect(f"{redirect_url}?{param}")

