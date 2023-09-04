"""
URL configuration for netflix_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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


# siteapp'in viewlerini çek
from netflix_app.views import *
# userapp'in viewlerini çek
from netflix_user_app.views import *
# netflix_Api viewleri
from netflix_api.views import *

# resim icin konfigürasyon
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # netflix_app
    path('', index, name="homepage"),
    # netflix_App burada biter

    # netflix_user_app
    path('login', user_login, name="user-login"),
    path('logout', user_logout, name="user-logout"),

    path('register', user_register, name="user-register"),
    path('browse', user_dashboard, name="user-dashboard"),
    path('profile/select', user_profile_select, name="user-profile-select"),
    path('genres/<categoryId>', only_film_or_shows, name="movie-category"),
    path('profile/<profileId>/my-list', userList, name="user-list"),
    path('YourAccount/<userId>', user_account, name="user-account"),
    path('YourAccount/change/settings', change_user_setting, name="change-user-setting"),
    path('YourAccount/change/card-detail', get_or_setCard, name="get-or-setCard"),
    # netflix_user_app burada biter

    # netflix_api 
    path("v1/api/movies/<movieId>/like", likeMovie, name="like-movie"),
    path("v1/api/movies/profiles/<profileId>/item/<movieId>/add", addList, name="add-list"),
    path("v1/api/movies/profiles/<profileId>/item/<movieId>/remove", removeList, name="remove-list")
    # netflix_api endpointleri biter
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
