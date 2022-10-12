from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.user_logout, name='userlogout'),
    path('login', views.user_login, name='userlogin'),
    path('', views.langingpage, name='homepage'),
    path('usersignup', views.usersignup, name='usersignup'),
    path('conformsingup', views.confirm_signup, name='confirm_signup'),
    path('otplogin', views.opt_login, name='otplogins'),
    path('confirmotplogin', views.confirm_otp_login, name='confirmotplogin'),
    path('dashboard', views.user_dashboard, name='userdashboard'),
    path('forgotpassword', views.forgot_password, name='forgotpassword'),
    path('forgotpasswordotp', views.otp_reset_password, name='otp_reset_password'),
    path('resetpassword', views.reset_password, name='reset_password'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('my_Cancel', views.my_Cancel, name='my_Cancel'),
    path('Edite_profile', views.Edite_Profile, name='Edite_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('OrderDetails/<int:order_number>/', views.Order_Details, name='OrderDetails'),
    path('OrderCancel/<int:order_number>/', views.Cancel_Order, name='OrderCancel'),
]
