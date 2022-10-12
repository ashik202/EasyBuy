from django.urls import path, include

from store import views

urlpatterns = [
    path('', views.storepage, name='storepage'),
    path('<slug:category_slug>/<slug:product_slug>/', views.singleproductpagr, name='single_product'),
    path('<slug:category_slug>/', views.storepage, name='product_by_category'),
    path('search',views.search,name='search')

]
