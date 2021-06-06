"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from .views import store, item_detail, signup,\
    add_to_cart, userlogin, userlogout

urlpatterns = [
    path('', store, name='store'),
    path('detail/<int:pk>/', item_detail, name='detail'),
    path('register/', signup, name='register'),
    path('login/', userlogin, name='login'),
    path('logout/', userlogout, name='logout'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
]
