"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index,name='index'),
    path('product/<str:cat>/', views.product,name='product'),
    path('shoping-cart/', views.cart,name='cart'),
    path('blog/', views.blog,name='blog'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('fpass/', views.fpass,name='fpass'),
    path('otp/', views.otp,name='otp'),
    path('newpassword/', views.newpassword,name='newpassword'), 
    path('cpassword/', views.cpassword,name='cpassword'), 
    path('profile/', views.profile,name='profile'), 
    path('fpass_email/', views.fpass_email,name='fpass_email'),
    path('verify_otp/', views.verify_otp,name='verify_otp'),
    path('new_password/', views.new_password,name='new_password'),
    path('add_product/', views.add_product,name='add_product'),
    path('sindex/', views.sindex,name='sindex'),
    path('view_product/<str:cat>/', views.view_product,name='view_product'),
    path('product_detail/ <int:pk>/', views.product_detail,name='product_detail'),
    path('pedit/ <int:pk>/', views.pedit,name='pedit'),
    path('pdelete/ <int:pk>/', views.pdelete,name='pdelete'),
    path('bpdetails/ <int:pk>/', views.bpdetails,name='bpdetails'),
    path('addwishlist/ <int:pk>/', views.addwishlist,name='addwishlist'),
    path('wishlist/', views.wishlist,name='wishlist'),
    path('delwishlist/ <int:pk>/', views.delwishlist,name='delwishlist'),
    path('addcart/ <int:pk>/', views.addcart,name='addcart'),
    path('cart/', views.cart,name='cart'),
    path('delcart/ <int:pk>/', views.delcart,name='delcart'),
    path('del_one_quantity', views.deleteOneQuantity,name='del_one_quantity'),
    path('add_one_quantity', views.addOneQuantity,name='add_one_quantity'),
    path('order_details', views.orderDetails,name='order_details'),
    path('checkout', views.Checkout,name='checkout'),
    path('success', views.success,name='success'),
    path('proceed-to-pay',views.razorpaycheck,name='proceed_to_pay'),
    path('my-orders/',views.myOrders,name='my_orders')
]
    