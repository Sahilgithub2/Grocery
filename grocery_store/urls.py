"""grocery_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from grocery_app import views
#from captcha.views import captcharefresh

from grocery_app import views

urlpatterns = [

    path('', views.index_view, name='index'),
    path('admin/', admin.site.urls),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('cart/', views.cart_view, name='cart'),
    path('fruits/', views.fruits_view, name='fruits'),
    path('vegetables/', views.vegetables_view, name='vegetables'),
    path('eggs/', views.eggs_view, name='eggs'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('index_view/', views.index_view, name='index_view'),
    path('add_product/', views.add_product, name='add_product'),
    path('view_products/', views.view_products, name='view_products'),
    path('captcha/', include('captcha.urls')),
    path('captcha/refresh/', views.captcha_refresh, name='captcha_refresh'),
    path('create-payment/', views.create_payment, name='create_payment'),
    path('products/category/<str:category>/', views.fetch_products_by_category, name='products_by_category'),
    path('products/subcategory/<str:subcategory>/', views.fetch_products_by_subcategory, name='products_by_subcategory')

]
