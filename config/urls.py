"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from core.views import home
from apps.companies.views import companies_list

from apps.connection_views import delete_connection

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', lambda request: redirect('/companies/')),

    path('companies/', include('apps.companies.urls'), name='companies'),
    path('contacts/', include('apps.contacts.urls')),
    path('materials/', include('apps.materials.urls')),
    path('connection_delete/', delete_connection)
]
