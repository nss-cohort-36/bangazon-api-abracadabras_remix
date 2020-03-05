"""bangazon_customer_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers
from bangazon_customer_api.views import register_user, login_user, ProductTypes, Products, Customers, Orders, PaymentTypes
from rest_framework.authtoken.views import obtain_auth_token
from bangazon_customer_api.models import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customers', Customers, 'customer')
router.register(r'orders', Orders, 'order')
router.register(r'products', Products, 'product')
router.register(r'paymenttypes', PaymentTypes, 'paymenttype')
router.register(r'producttypes', ProductTypes, 'producttype')
# router.register(r'users', User, 'user')
# router.register(r'orderproducts', OrderProducts, 'orderproduct')

urlpatterns = [
    path('', include(router.urls)),
    path('admin', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth', obtain_auth_token),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
