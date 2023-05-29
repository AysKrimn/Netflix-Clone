from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

# gerekli formları al
from .form import *
from .models import *

# Create your views here.
def user_login(request):

    if request.method == 'POST':
        # user login olmak istiyo 
        username = request.POST.get('email')
        password = request.POST.get('password')

        if username and password:
            # user kontrolü yap
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                # film sekmesine yönlendir.
                return redirect('browse-profile')
    else:
        # get istekleri
        # eğer kullanıcı giriş yapmışsa burayı görmesini engelle
        if request.user.is_authenticated:
             return redirect('browse-profile')
        
        # login olmamışsa login olsun:
        return render(request, 'login.html')


# hesapların seçildiği alan
def browseProfile(request):
    context = {}
    
    form = CreateProfile()

    if request.method == 'POST':
        form = CreateProfile(request.POST, request.FILES)
        # verileri oluştur ama veritabanına kayıt etme
        instances = form.save(commit=False)
        instances.user = request.user
        instances.save()
        # aynı sayfaya yönlendir
        return redirect('browse-profile')
    else:
        # get istekleri
          context['form'] = form
          context['profiles'] = NetflixProfile.objects.filter(user_id=request.user.id)
          return render(request, 'browseProfile.html', context)


# filmlerin yüklendiği sayfa (feed)
def boardIndex(request, profileId):
    context = {}
   
    selectedProfile = NetflixProfile.objects.filter(id=profileId).first()
    context['profile'] = selectedProfile

    # spesifik olarak siralama isteği gelmiş mi?
    contentType = request.GET.get('sirala')
    print("tür:", contentType)
    if contentType:
        if contentType == 'diziler':
             context['diziler'] = Movies.objects.filter(movie_type=2)

        if contentType == 'filmler':
             context['filmler'] = Movies.objects.filter(movie_type=1)
    else:
        # content type yoksa hepsini gönder
        # filmler
        context['filmler'] = Movies.objects.filter(movie_type=1).order_by('?')
        context['diziler'] = Movies.objects.filter(movie_type=2).order_by('?')



    return render(request, 'browse-index.html', context)


# userin favorileri
def my_list(request, profileId):
    context = {}
    
    selectedProfile = NetflixProfile.objects.filter(id=profileId).first()
    context['profile'] = selectedProfile

    context['movies'] =  selectedProfile.movie.all()
    # favoriye eklenen dizi ve filmleri gönder


    return render(request, 'myList.html', context)


# hesap ayarları
def account_setting(request):
    context = {}

    profileId = request.GET.get('watch')
    
    context['profile'] = NetflixProfile.objects.filter(id=profileId).first()




    return render(request, 'hesap.html', context)


# user çıkış yapmışsa
def user_logout(request):

    if request.user.is_authenticated:
        logout(request)
        return redirect('anasayfa')
    
    else:
        return redirect('user_login')
    







# api viewi
from django.http import JsonResponse
def addFavouriteList(request, profileId, movieId):
    
    result = {}

    print("endpointe gelen data:",profileId, movieId)

    # profileId ve movieId veritabanında ara ve gerekli işlemleri yap.
    selectedProfile = NetflixProfile.objects.filter(id=profileId).first()
    selectedMovie = Movies.objects.filter(id=movieId).first()

    if selectedProfile is None:
      result['status'] = "Böyle bir kullanici bulunamadi"
    
    # film ve kullanici varsa
    if selectedProfile and selectedMovie:
       # kullanıcının favori listesine ekle
       selectedProfile.movie.add(selectedMovie)    
       result['status'] = "Basarili"

    return JsonResponse(result)



def removeFavouriteList(request, profileId, movieId):
    result = {}

    result['status'] = 'Başarılı bir şekilde çıkarıldı'
    return JsonResponse(result)