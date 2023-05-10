"""netflixProje URL Configuration

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
# resim ayarları
from django.conf import settings
from django.conf.urls.static import static

# viewsleri import et
from netflixApp.views import *
from userApp.views import *
from netflixApi.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='anasayfa'),


    # userApp views
    path('giris-yap', user_login, name="giris-yap"),
    path('board/index', user_main_browse_page, name='browse'),
    path('listem', myList, name="listem"),


    # api
    path('api/v1/set-list/<movieId>/<userId>', movie_set, name='movie-set-api')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
