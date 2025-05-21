"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from polls import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html', next_page="/products/"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'),
         name='logout'),
    path('', views.home, name='home'),
    path('products/', views.product_list , name='product_list'),
    path('signup/', views.signup_view, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart_view, name='cart'), 
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),  
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.process_payment, name='payment'),
    path('order_history/', views.order_history, name='order_history'),
    path('clear_cart/', views.clear_cart, name='clear_cart')
]
