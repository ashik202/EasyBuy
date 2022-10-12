from django.urls import path, include

from admin_app import views

urlpatterns = [
    # login of admin
    path('', views.adminlogin, name='adminlogin'),
    # admin home page

    path('adminhome', views.adminhome,name='adminhome'),

    # logout of agmin
    path('adminlogout', views.adminlout, name='adminlogout'),

    # admin category functions
    path('adminviewcategory', views.adminviewcategory, name='adminviewcategory'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('editcategory/<int:id>/', views.editcategory, name='editcategory'),
    path('deletecategory/<int:id>/', views.deletecategory, name='deletecategory'),

    # admin brand functions
    path('adminviewbrand', views.adminviewbrand, name='adminbrand'),
    path('addbrand', views.addbrand, name='addbrand'),
    path('editbrand/<int:id>/', views.editbrand, name='editbrand'),
    path('deletebrand/<int:id>/', views.deletebrand, name='deletebrand'),

    # admin product functions
    path('adminviewproduct', views.adminviewproduct, name='adminviewproduct'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('editproduct/<int:id>/', views.editproduct, name='editproduct'),
    path('deleteproduct/<int:id>/', views.deleteproduct, name='deleteproduct'),

    path('view_variation', views.View_Variation, name='view_variation'),
    path('delete_variation/<int:id>/', views.Delete_Variation, name='delete_variation'),
    path('Add_variation', views.Add_variation, name='Add_variation'),

    # user management
    path('adminviewuser', views.adminviewuser, name='adminviewuser'),
    path('blockuser/<int:id>/', views.blockuser, name='blockuser'),
    path('unblockuser/<int:id>/', views.unblockuser, name='unblockuser'),

    # admin coupon
    path('viewcoupon', views.adminviewcoupon, name='viewcoupon'),
    path('deletecoupon/<int:id>/', views.deletecoupon, name='deletecoupon'),
    path('addcoupon', views.addcoupon, name='addcoupon'),

    # admin orders
    path('adminorder', views.OrderProductView, name='OrderView'),
    path('orderdetailview/<int:id>/', views.OrderDetailView, name='OrderDetailView'),
    path('orderstatuschange/<int:id>/', views.Update_Order_status, name='Updateorderstatus'),

    # offer
    path('admin_brandoffer', views.View_Brand_Offer, name='view_admin_brand_offer'),
    path('admin_categoryoffer', views.View_Category_Offer, name='view_admin_category_offer'),
    path('admin_productoffer', views.View_Product_Offer, name='view_admin_product_offer'),
    path('admin_delet_product_offer/<int:id>/', views.Delete_Product_Offer, name='deleteproductoffer'),
    path('admin_delet_category_offer/<int:id>/', views.Delete_Category_Offer, name='deletecategoryoffer'),
    path('admin_delet_brand_offer/<int:id>/', views.Delete_Brand_Offer, name='deletebrandoffer'),
    path('admin_Add_Product_offer', views.Add_Product_offer, name='Add_Product_offer'),
    path('admin_Add_Category_offer', views.Add_Category_offer, name='Add_Category_offer'),
    path('admin_Add_Brand_offer', views.Add_Brand_offer, name='Add_Brand_offer'),
    path('Sales_Report', views.Sales_Report, name='Sales_Report'),
    path('Exel_convetion', views.sales_export_csv, name='Exel_convetion'),

]
