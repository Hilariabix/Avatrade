"""
Avatrade URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/', include('avatrade.social_network.urls')),
    path('api/jwtauth/', include('avatrade.jwtauth.urls'), name='jwtauth'),
]
