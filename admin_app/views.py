import calendar
import csv

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control

from cart.form import Couponform
from cart.models import Coupon
from category.models import category
from category.form import categoryform
from brand.models import brand
from brand.form import brandform
from orders.models import Order, OrderProduct
from product.models import product, Variation
from product.form import productform, variationform
from accounts.models import Account
from offer.models import CategoryOffer,ProductOffer,BrandOffer
from offer.form import BrandOfffer_form,ProductOffer_form,CategoryOffer_form



# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if 'admin' in request.session:
        return redirect('adminhome')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superadmin:
                request.session['admin'] = username
                print(request.session['admin'])
                login(request, user)
                return redirect('adminhome')
        else:
            messages.error(request, 'invalid credentials')
            return redirect(adminlogin)

    return render(request, 'admin/adminlogin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminhome(request):
    if 'admin' in request.session:
        New = 0
        Accepted = 0
        Cancelled = 0
        Completed = 0
        income = 0
        orders = Order.objects.all()
        for order in orders:
            income += order.order_total

        labels = []
        data = []
        orders = OrderProduct.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month', 'count')

        labels = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'september']
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for d in orders:
            labels.append(calendar.month_name[d['month']])
            data.append([d['count']])
        labels1 = []
        data1 = []

        queryset = Order.objects.all()
        for i in queryset:
            if i.status == 'New':
                New += 1
            elif i.status == 'Accepted':
                Accepted += 1
            elif i.status == 'Cancelled':
                Cancelled += 1
            elif i.status == 'Completed':
                Completed += 1

        labels1 = ['New', 'Accepted', 'Cancelled', 'Completed']
        data1 = [New, Accepted, Cancelled, Completed]

        order_count = OrderProduct.objects.count()
        product_count = product.objects.count()
        print(product_count)
        cat_count = category.objects.count()
        user_count = Account.objects.count()

        categorys = category.objects.all().order_by('-id')[:5]
        products = product.objects.all().order_by('-id')[:5]
        orderproducts = OrderProduct.objects.all().order_by('-id')[:5]

        context = {
            'cat_count': cat_count,
            'product_count': product_count,
            'order_count': order_count,
            'labels1': labels1,
            'data1': data1,

            'labels': labels,
            'data': data,

            'category': categorys,
            'products': products,
            'orderproducts': orderproducts,
            'income': income,
            'user_count': user_count

        }
        return render(request, 'admin/Admin_home.html',context)
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlout(request):
    if 'admin' in request.session:
        request.session.flush()
        logout(request)
    return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminviewcategory(request):
    if 'admin' in request.session:
        search_key = request.GET.get('key') if request.GET.get('key') is not None else ''
        data = category.objects.all().order_by('id') and category.objects.filter(
            Q(category_name__icontains=search_key) or Q(description__icontains=search_key))
        return render(request, 'admin/admincategory.html', {'datas': data})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcategory(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            category_form = categoryform(request.POST, request.FILES)
            if category_form.is_valid():
                category_form.save()
            return redirect(adminviewcategory)
        category_form = categoryform()

        return render(request, 'admin/addcategory.html', {'category_form': category_form})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecategory(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pi = category.objects.get(pk=id)
            pi.delete()
            return redirect(adminviewcategory)

        return render(request, 'admin/addcategory.html')
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminviewbrand(request):
    if 'admin' in request.session:
        search_key = request.GET.get('key') if request.GET.get('key') is not None else ''
        data = brand.objects.all() and brand.objects.filter(
            Q(brand_name__icontains=search_key) or Q(description__icontains=search_key))

        return render(request, 'admin/adminbrand.html', {'datas': data})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addbrand(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            brand_form = brandform(request.POST, request.FILES)
            if brand_form.is_valid():
                brand_form.save()
            return redirect(adminviewbrand)
        brand_form = brandform()

        return render(request, 'admin/addbrand.html', {'brand_form': brand_form})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletebrand(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pi = brand.objects.get(pk=id)
            pi.delete()
            return redirect(adminviewbrand)


    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminviewproduct(request):
    if 'admin' in request.session:
        search_key = request.GET.get('key') if request.GET.get('key') is not None else ''
        data = product.objects.all() and product.objects.filter(
            Q(product_name__icontains=search_key) or Q(description__icontains=search_key))
        return render(request, 'admin/adminviewproduct.html', {'datas': data})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addproduct(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            product_form = productform(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
            return redirect(adminviewproduct)
        product_form = productform()
        return render(request, 'admin/addproduct.html', {'product_form': product_form})


    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteproduct(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pr = product.objects.get(pk=id)
            pr.delete()
            return redirect(adminviewproduct)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editproduct(request, id):
    if 'admin' in request.session:
        data = product.objects.get(pk=id)
        form = productform(instance=data)
        if request.method == 'POST':
            form = productform(request.POST, request.FILES, instance=data)
            if form.is_valid():
                form.save()
                return redirect(adminviewproduct)

        else:
            return render(request, 'admin/editproduct.html', {'form': form})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editcategory(request, id):
    if 'admin' in request.session:
        data = category.objects.get(pk=id)
        form = categoryform(instance=data)
        if request.method == 'POST':
            form = categoryform(request.POST, request.FILES, instance=data)
            if form.is_valid():
                form.save()
                return redirect(adminviewcategory)

        else:
            return render(request, 'admin/editcategory.html', {'forms': form})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editbrand(request, id):
    if 'admin' in request.session:
        data = brand.objects.get(pk=id)
        form = brandform(instance=data)
        if request.method == 'POST':
            form = brandform(request.POST, request.FILES, instance=data)
            if form.is_valid():
                form.save()
                return redirect(adminviewbrand)

        else:
            return render(request, 'admin/editbrand.html', {'forms': form})
    else:
        return redirect(adminlogin)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminviewuser(request):
    if 'admin' in request.session:
        user = Account.objects.filter(is_superadmin=False)
        return render(request, 'admin/adminuserview.html', {'data': user})


def unblockuser(request, id):
    if 'admin' in request.session:
        print(id)
        user = Account.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect(adminviewuser)


def blockuser(request, id):
    if 'admin' in request.session:
        print(id)

        user = Account.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect(adminviewuser)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminviewcoupon(request):
    if 'admin' in request.session:
        search_key = request.GET.get('key') if request.GET.get('key') is not None else ''
        data = Coupon.objects.all() and Coupon.objects.filter(
            Q(coupon_code__icontains=search_key) or Q(coupon_name__icontains=search_key))
        return render(request, 'admin/admincoupon.html', {'datas': data})
    else:
        return redirect(adminlogin)


def deletecoupon(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pr = Coupon.objects.get(pk=id)
            pr.delete()
            return redirect(adminviewcoupon)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcoupon(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            coupon_form = Couponform(request.POST, request.FILES)
            if coupon_form.is_valid():
                coupon_form.save()
            return redirect(adminviewcoupon)
        coupon_form = Couponform()
        return render(request, 'admin/addcoupon.html', {'coupon_form': coupon_form})


    else:
        return redirect(adminlogin)


def OrderProductView(request):
    if 'admin' in request.session:

        order = Order.objects.all()
        context = {
            'orders': order
        }
        return render(request, 'admin/orderview.html', context)
    else:
        return redirect('adminlogin')


def OrderDetailView(request, id):
    if 'admin' in request.session:
        print("number\n\n\n",id)
        orderproducts = OrderProduct.objects.filter(order=id).order_by('-id')
        print(list(orderproducts))
        return render(request, 'admin/orderdetailview.html', {'orders': orderproducts})


    else:
        return redirect('adminlogin')

def Update_Order_status(request,id):
    if 'admin' in request.session:
        if request.method=='POST':
            status=request.POST['status']
            data=Order.objects.get(id=id)
            data.status=status
            data.save()
            return redirect('OrderView')

    else:
        return redirect('adminlogin')



def View_Variation(request):
    if 'admin' in request.session:
       variation = Variation.objects.all()
       return render(request,'admin/view_variations.html',{'variations':variation})

    else:
        return redirect('adminlogin')

def Delete_Variation(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pr = Variation.objects.get(pk=id)
            pr.delete()
            return redirect('view_variation')




def Add_variation(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            variation_form = variationform(request.POST, request.FILES)
            if variation_form.is_valid():
                variation_form.save()
                return redirect('view_variation')
        variation_form=variationform()
        return render(request,'admin/Add_variation.html',{'variationform':variation_form})
    else:
        return redirect('_variation')




def View_Brand_Offer(request):
    if 'admin' in request.session:
       brandoffer = BrandOffer.objects.all()
       return render(request,'admin/view_brandoffer.html',{'brandoffer':brandoffer})

    else:
        return redirect('adminlogin')

def View_Category_Offer(request):
    if 'admin' in request.session:
       brandoffer = CategoryOffer.objects.all()
       return render(request,'admin/view_category_offer.html',{'brandoffer':brandoffer})

    else:
        return redirect('adminlogin')


def View_Product_Offer(request):
    if 'admin' in request.session:
       brandoffer = ProductOffer.objects.all()
       return render(request,'admin/view_product_offer.html',{'brandoffer':brandoffer})

    else:
        return redirect('adminlogin')

def Delete_Category_Offer(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pr = CategoryOffer.objects.get(pk=id)
            pr.delete()
            return redirect('view_admin_category_offer')

def Delete_Brand_Offer(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pr = BrandOffer.objects.get(pk=id)
            pr.delete()
            return redirect('view_admin_brand_offer')

def Delete_Product_Offer(request, id):
    if 'admin' in request.session:
        if request.method == 'POST':
            pr = ProductOffer.objects.get(pk=id)
            pr.delete()
            return redirect('view_admin_product_offer')


def Add_Product_offer(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            product_form = ProductOffer_form(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                return redirect('view_admin_product_offer')
        product_form=ProductOffer_form()
        return render(request,'admin/Add_Product_Offer.html',{'product_form':product_form})
    else:
        return redirect('adminlogin')


def Add_Category_offer(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            category_form = CategoryOffer_form(request.POST, request.FILES)
            if category_form.is_valid():
                category_form.save()
                return redirect('view_admin_category_offer')
        category_form=CategoryOffer_form()
        return render(request,'admin/Add_Category_Offer.html',{'category_form':category_form})
    else:
        return redirect('adminlogin')


def Add_Brand_offer(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            brand_form = BrandOfffer_form(request.POST, request.FILES)
            if brand_form.is_valid():
                brand_form.save()
                return redirect('view_admin_brand_offer')
        brand_form=BrandOfffer_form()
        return render(request,'admin/Add_Brand_Offer.html',{'brand_form':brand_form})
    else:
        return redirect('adminlogin')


def Sales_Report(request):
    if 'admin' in request.session:
        products=product.objects.all()
        return render(request,'admin/admin_sales_report.html',{'products':products})
    else:
        return redirect('adminlogin')



def sales_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=products.csv"

    writer = csv.writer(response)
    products = product.objects.all()

    writer.writerow(
        [

            "Product",
            "Brand",
            "Category",
            "Stock",
            "Price",
            "Sales Count",
            "Revenue",

        ]
    )

    for Product in products:
        writer.writerow(
            [

                Product.product_name,
                Product.brand,
                Product.category,
                Product.stock,
                Product.price,
                Product.get_count()[0]["quantity"],
                Product.get_revenue()[0]["revenue"],


            ]
        )
    return response