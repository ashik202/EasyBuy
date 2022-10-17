from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from category.models import category
from product.models import product, ProductGallery
from cart.models import Cartitem, Cart
from cart.views import _cart_id


# Create your views here.

def storepage(request, category_slug=None):
    categories = None
    data = None
    if category_slug is not None:
        print('slug')
        categories = get_object_or_404(category, slug=category_slug)
        data = product.objects.filter(category=categories, is_available=True)
        for products in data:
            if products.Offer_Price():
                new = product.Offer_Price(products)
                products.new_price = new["new_price"]
                products.discount = new["discount"]
                products.save()
            else:
                products.new_price = 0
                products.discount=0
                products.save()
        paginator = Paginator(data, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        datacound = data.count()
    else:

        data = product.objects.all().filter(is_available=True)
        for products in data:
            if products.Offer_Price() :
                print("truve")
                new = product.Offer_Price(products)
                products.new_price = new["new_price"]
                products.discount = new["discount"]
                products.save()
                print(products.new_price)
                print(products.discount)
            else:
                print('else print')
                products.new_price = 0
                products.discount = 0

                products.save()
        paginator = Paginator(data, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        datacound = data.count()

    context = {
        'data': paged_product,
        'datacound': datacound,
    }

    return render(request, 'storetem/store.html', context)


def singleproductpagr(request, category_slug, product_slug):
    try:
        single_product = product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request), products=single_product).exists()
        product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    except Exception as e:
        raise e
    return render(request, 'storetem/singleproduct.html',
                  {'data': single_product, 'in_cart': in_cart, 'product_gallery': product_gallery})


def search(request):
    if "key" in request.GET:
        keyword = request.GET["key"]
        if keyword:
            products = product.objects.order_by("id").filter(
                Q(description__icontains=keyword)
                | Q(product_name__icontains=keyword)
            )

            # q means query set

        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        datacound = products.count()

        context = {
            'data': paged_product,
            'datacound': datacound,
        }
        return render(request, 'storetem/store.html', context)
