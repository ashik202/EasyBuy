from pyexpat.errors import messages
from django.contrib.auth import login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.contrib import messages, auth

from accounts.models import Account, UserProfile
from cart.models import Cart, Cartitem
from orders.models import Order, OrderProduct
from accounts.form import UserForm, UserProfileForm

from user_app.form import RegistrationForm
from product.models import product
from user_app.verify import sentOTP, checkOTP
from cart.views import _cart_id
import requests

from django.http import HttpResponse


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_active == True:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = Cartitem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = Cartitem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    cart_item = Cartitem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        exising_variation = item.variations.all()
                        ex_var_list.append(list(exising_variation))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = Cartitem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = Cartitem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            login(request, user)
            request.session['email'] = email
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)


            except:
                return redirect(user_dashboard)

        else:
            messages.error(request, 'invalid credentials')
            return redirect(user_login)
    return render(request, 'user/userlogin.html')


def langingpage(request):
    data = product.objects.all
    return render(request, 'storetem/home.html', {'data': data})


def user_signup(request):
    global phone_number
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # to fetch the data from request
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]

            request.session["first_name"] = first_name
            request.session["last_name"] = last_name
            request.session["email"] = email
            request.session["checkmobile"] = phone_number
            request.session["password"] = password
            request.session["username"] = username
            sentOTP(phone_number)
            return redirect('confirm_signup')
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "user/usersignup.html", context)


def confirm_signup(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == "POST":
        otp = request.POST["otpcode"]
        phone_number = request.session["checkmobile"]
        print(otp)
        if checkOTP(phone_number, otp):
            first_name = request.session["first_name"]
            last_name = request.session["last_name"]
            email = request.session["email"]
            phone_number = request.session["checkmobile"]
            password = request.session["password"]
            username = request.session["username"]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username,

            )
            user.is_active = True
            user.phone_number = phone_number
            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = "static/default.png"
            profile.save()
            user.save()

            return redirect("userlogin")
        else:
            print("OTP not matching")
            return redirect("confirm_signup")
    return render(request, "user/confirm_signup.html")


def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect(langingpage)


def opt_login(request):
    if request.method == 'POST':
        phone = request.POST['number']
        user = Account.objects.filter(phone_number=phone)
        if user is not None:
            request.session['numberlogin'] = phone
            sentOTP(phone)
            return redirect(confirm_otp_login)
    return render(request, 'user/optlogin.html')


def confirm_otp_login(request):
    if request.method == 'POST':
        otp = request.POST["otpcode"]
        number = request.session['numberlogin']
        if checkOTP(number, otp):
            user = Account.objects.get(phone_number=number)
            if user is not None:
                login(request, user)
                request.session['email'] = user.email
                return redirect(user_dashboard)
    return render(request, 'user/confirmotplogin.html')


def user_dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    order_count = orders.count()
    context = {
        'order_count': order_count
    }
    return render(request, 'user/dashboard.html', context)


def my_orders(request):
    orders = Order.objects.filter(
        user=request.user, is_ordered=True
    ).order_by("-created_at")
    context = {"orders": orders}
    return render(request, "user/my_orders.html", context)

def my_Cancel(request):
    orders = Order.objects.filter(
        user=request.user, is_ordered=False
    ).order_by("-created_at")
    context = {"orders": orders}
    return render(request, "user/my_cancel.html", context)


def Edite_Profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render(request, 'user/Edite_Profile.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        number = request.POST['phone']
        user = Account.objects.get(phone_number=number, email=email)
        if user is not None:
            request.session['number_for_reset'] = number
            request.session['email'] = email
            sentOTP(number)
            return redirect(otp_reset_password)
        else:
            messages.error(request, 'invalid credentials')

    return render(request, 'user/forgotpassword.html')


def otp_reset_password(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        number = request.session['number_for_reset']
        if checkOTP(number, otp):
            return redirect(reset_password)
        else:
            messages.error(request, 'invalid otp')
    return render(request, 'user/otpresetpassword.html')


def reset_password(request):
    if request.method == 'POST':

        password = request.POST['password']
        number = request.session['number_for_reset']
        email = request.session['email']
        print(password)
        user = Account.objects.get(email=email, phone_number=number)
        print(user.username)
        user.set_password(password)
        user.save()
        if user.check_password(password):
            print('password match')
        else:
            print('password not match')
        return redirect(user_login)
    return render(request, 'user/resetpassword.html')


def change_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # logout(request)
            messages.success(request, "Password Updated Successfully.")
            return redirect('change_password')

        else:
            messages.error(request, "Your Existing Password Is Incorrect")
            return redirect('change_password')

    else:
        messages.info(request, "Password Does Not Match!")

    return render(request, "user/change_password.html")


def Order_Details(request, order_number):
    orderdetails = OrderProduct.objects.filter(order__order_number=order_number)
    order = Order.objects.get(order_number=order_number)
    sub_total = 0
    for i in orderdetails:
        sub_total += i.product_price * i.quantity

    context = {
        'subtotal': sub_total,
        'orderdetails': orderdetails,
        'order': order

    }
    return render(request, 'user/OrderDetail.html', context)


def Cancel_Order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.is_ordered = False
    order.status = "Canceled"
    order.save()
    return redirect('my_orders')


