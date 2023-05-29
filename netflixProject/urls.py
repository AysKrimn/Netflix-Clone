"""netflixProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


# applerden viewleri çek
from netflixApp.views import *
from userApp.views import *

# settingsden gelen dosyalar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="anasayfa"),

    # userApp uygulamasının endpointleri
    path('login', user_login, name="user_login"),
    path('watch/<profileId>', boardIndex, name="browse-movies"), 
    path('watch/mylist/<profileId>', my_list, name="my-list"), 
    path('browseProfile', browseProfile, name='browse-profile'),
    path('hesap', account_setting, name="account-setting"),
    path('logout', user_logout, name='user_logout'),


    # api
    path('api/v1/users/<profileId>/setItem/<movieId>', addFavouriteList, name='add-list'),
    path('api/v1/users/<profileId>/removeItem/<movieId>', addFavouriteList, name='remove-list')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
