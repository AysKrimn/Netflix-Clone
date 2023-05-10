from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# modelleri çağır
from .models import *
# Create your views here.
def user_login(request):

    # eğer metot post ise
    if request.method == 'POST':

        # usernamei ve sifreyi cek
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            print("veriler:", username, password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
               login(request, user)
               # anasayfaya yönlendir
            else:
            # hata mesajı ver
             return redirect('giris-yap')
                   
        # user başarılı bir şekilde login olmuşsa
        return redirect('browse')
    
    else:
     # get istekleri
     return render(request, 'login.html')


# filmlerin/dizilerin gösterildigi alan
def user_main_browse_page(request):
    context = {}
    sadeceDiziler = request.GET.get('dizi')
    sadeceFilmler = request.GET.get('film')

    print("request:", sadeceDiziler)
    # filmleri ayarla
    filmler = Movie.objects.filter(movie_type=2)
    # dizileri al
    diziler = Movie.objects.filter(movie_type=1)

    if sadeceDiziler:
       context['diziler'] = diziler

    if sadeceFilmler:
       context['filmler'] = filmler

    # eğer sadeceDiziler ve filmler yoksa
    if sadeceDiziler is None and sadeceFilmler is None:
        # filmleri ve dizileri beraber gönder
        context['filmler'] = filmler
        context["diziler"] = diziler


    return render(request, 'browse-movies.html', context)
# userin listem kısmı
def myList(request):
    context = {}
    # kullanıcının listesini döndür
    liste = request.user.movie_list.all()
    context['data'] = liste
   
    return render(request, 'listem.html', context)