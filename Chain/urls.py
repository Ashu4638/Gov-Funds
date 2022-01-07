"""Blockchain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from Chain import  views

urlpatterns = [
    path('', views.index, name='Home'),
    path('transaction', views.createTransaction, name="Transaction"),
    path('about', views.about, name="About"),
    path('contact', views.contact, name="Contact"),
    path('register', views.register, name="Register"),
    path('signup', views.singup, name="Signup"),
    path('loginform', views.loginform, name="loginform"),
    path('login', views.handlelogin, name="Login"),
    path('logout', views.handlelogout, name="Logout"),
    path('mine', views.Mine, name="Mine"),
    path('admin', views.admin, name="Admin"),
    path('addblock', views.addblock, name="addblock"),
    path('viewblockchain', views.viewblockchain, name="viewblockchain"),
    path('viewtransaction', views.viewtransaction, name="viewtransaction"),
    path('addfund', views.addfund, name="addfund"),
    path('appendfund', views.appendfund, name="addfund"),
    path('deleteTransaction', views.deleteTransaction, name="deleteTransaction"),
    path('editfund', views.editfund, name="editfund"),
    path('deletefund', views.deletefund, name="deletefund"),
    path('updatefund', views.updatefund, name="updatefund"),
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
