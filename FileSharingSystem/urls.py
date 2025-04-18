"""
URL configuration for FileSharingSystem project.

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
from django.urls import path
from . import views
from .views import upload_files


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.loginpage,name='login'),
    path('register/',views.registerpage,name='register'),
    path('',views.homepage,name='home'),
    path('logout/',views.logout_page,name='logout'),
    path('upload_files/',views.upload_files,name='upload_file'),
    path('files/', views.file_list, name='file_list'),  # URL for uploaded file list



    
]
