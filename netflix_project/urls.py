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

# static & settingpy
from django.conf import settings
from django.conf.urls.static import static

# viewleri çek
from netflix_app.views import *
from user_app.views import *
from netflix_api.views import *
from sql_test_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="home"),

    # userapp endpointleri
    path('browse', user_dashboard, name="dashboard"),
    path("login", user_login, name="user_login"),
    path("register", user_register, name="user_register"),
    path("reset", user_reset_password, name="user_reset"),
    path("logout", user_logout, name="user_logout"),
    path('YourAccount', user_account_setting, name="user-account"),
    path('change/user/account/details', change_user_setting, name="change-user-setting"),
    path("myList", loadMyList, name="my_list"),
    path("select/profile", user_profile_select, name="user_profile_select"),
    path("genres/<categoryId>", only_movies, name="only_movies"),
    
    # userapp endpointleri biter

    # sql_test_app endpointler başlar
    path("application/test/personel", return_all_personel),
    path("application/test/personel/delete", remove_person),
    path("application/test/personel/create", create_person),
    path("application/test/personel/update", update_person),
    # sql_test_app endpointleri burada biter

    # api endpoints
    path("api/v1/movies/<movieId>/like", like_movie, name="like_movie"),
    path("api/v1/myList/<movieId>/add", addMyList, name="addMyList"),
    path("api/v1/myList/<movieId>/remove", removeMyList, name="removeMyList"),
    path("api/v1/activate/kid/protection", kidProtect, name="kidProtect"),
    path("api/v1/user/subscription", canceloractiveSub, name="sub")
    # api endpoints biter
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
