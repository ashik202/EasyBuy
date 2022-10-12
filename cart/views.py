from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from product.models import product, Variation

from .models import Cartitem, Cart, Coupon
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user=request.user
    products = product.objects.get(id=product_id)
    #if user is authenticated

    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=products, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    print(variation)
                    product_variation.append(variation)

                except:

                    pass


        is_cart_item_exists = Cartitem.objects.filter(products=products, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(products=products, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                exising_variation = item.variations.all()
                ex_var_list.append(list(exising_variation))
                id.append(item.id)
            print(ex_var_list)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Cartitem.objects.get(products=products, id=item_id)
                item.quantity += 1
                item.save()
            else:

                item = Cartitem.objects.create(products=products, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                    # cart_item.quantity += 1
                    item.save()
        else:
            items = Cartitem.objects.create(
                products=products,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                items.variations.clear()

                items.variations.add(*product_variation)

            items.save()

        return redirect('cartpage')




    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=products, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    print(variation)
                    product_variation.append(variation)

                except:

                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))

        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
        is_cart_item_exists = Cartitem.objects.filter(products=products, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(products=products, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                exising_variation = item.variations.all()
                ex_var_list.append(list(exising_variation))
                id.append(item.id)
            print(ex_var_list)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Cartitem.objects.get(products=products, id=item_id)
                item.quantity += 1
                item.save()
            else:

                 item = Cartitem.objects.create(products=products, quantity=1, cart=cart)
                 if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                    # cart_item.quantity += 1
                    item.save()
        else:
            cart_item = Cartitem.objects.create(
                products=products,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()

                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect('cartpage')


def remove_cart(request, product_id,cart_item_id):

    products = get_object_or_404(product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=Cartitem.objects.get(products=products,user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cartitem.objects.get(products=products, cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity = cart_item.quantity - 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cartpage')


def remove_cart_item(request, product_id,cart_item_id):
    products = get_object_or_404(product, id=product_id)
    if request.user.is_authenticated:
        cart_item = Cartitem.objects.get(products=products, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cartitem.objects.get(products=products, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cartpage')


def cart(request, total=0, quntity=0, cart_items=None):
    try:
        reduction=0
        tax = 0
        granttotal = 0
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(user=request.user,is_active=True)
            if 'coupon_code' in request.session:
                print(request.session['coupon_code'])

                coupon = Coupon.objects.get(coupon_code=request.session['coupon_code'])
                reduction = coupon.amount
                print(reduction)
                a = cart_items.count()
                if a <= 0:
                    del request.session['coupon_code']

            else:
                reduction = 0
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.products.new_price !=0:
                total = total + (cart_item.products.new_price * cart_item.quantity)
            else:

                total = total + (cart_item.products.price * cart_item.quantity)
            quntity = quntity + cart_item.quantity
            tax = (18 * total) / 100
            granttotal = total + tax-reduction
    except ObjectDoesNotExist:
        pass


    print(granttotal)

    context = {
        'total': total,
        'quntity': quntity,
        'cart_items': cart_items,
        'tax': tax,
        'granttotal': granttotal

    }

    return render(request, 'cart/cartview.html', context)

@login_required(login_url='userlogin')
def checkout(request, total=0, quntity=0, cart_items=None):
    tax = 0
    granttotal = 0
    try:
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user, is_active=True)


            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.products.new_price !=0:
                total = total + (cart_item.products.new_price * cart_item.quantity)
            else:
                total = total + (cart_item.products.price * cart_item.quantity)
            quntity = quntity + cart_item.quantity
            tax = (18 * total) / 100
            granttotal = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quntity': quntity,
        'cart_items': cart_items,
        'tax': tax,
        'granttotal': granttotal

    }
    return render(request,'cart/checkout.html',context)


class UsedCoupon:
    pass


def couponapply(request):
    if request.method == 'POST':

        coupon_code = request.POST.get('coupon')
        print(coupon_code)

        try:
            if Coupon.objects.get(coupon_code=coupon_code):
                coupon_exist = Coupon.objects.get(coupon_code=coupon_code)
                try:

                    if UsedCoupon.objects.get(user=request.user, coupon=coupon_exist):
                        print('fail')
                        messages.error(request, "coupon already used")

                        return redirect(cart)


                except:
                    print('pass')
                    request.session['coupon_code'] = coupon_code
                    print(request.session['coupon_code'])

        except:
            pass
    return redirect(cart)