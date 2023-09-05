from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import * 

# profil oluşturma formu
from .form import CreateProfile

# Create your views here.
def user_login(request):


    if request.method == 'POST':
        user_username = request.POST.get('user_username')
        user_password = request.POST.get('user_password')

        if user_username and user_password:

            user = authenticate(request,  username=user_username, password=user_password)

            if user:
                login(request, user)
                return redirect('user_profile_select')
            
        # diğer tüm potensiyel hatalar içni:
        return redirect('user_login')
    else:
        return render(request, 'login.html')

def user_logout(request):

    if request.user.is_authenticated:
        logout(request)

    response = redirect('home')
    # cookie çıkartır
    response.delete_cookie("selected_profile")
        
    return response
    

# hesap oluşturma
def user_register(request):

    if request.method == 'POST':
        
        user_name = request.POST.get('user_username')
        user_email = request.POST.get('user_email')
        user_password = request.POST.get('user_password')

        if user_name and user_email and user_password:
            print("debug password:", user_password)
            # böyle bir user var mı?
            isRegisteredEmail = NetflixUser.objects.filter(email = user_email).first()

            if isRegisteredEmail:
                # hata mesajı
                return redirect("user_register")


            user = NetflixUser.objects.create(username = user_name, email = user_email)
            user.set_password(user_password)
            user.save()

            # set_password ile veritabanına şifreyi hashlenmiş bir şekilde gönder


            # mesaj gönderilebilir
            return redirect('user_login')

    else:
        return render(request, 'register.html')
    


# filmlerin izlendigi yer
# bu endpointi koru
@login_required(login_url="user_login")
def user_dashboard(request):
    context = {}
    
    movies = {}

    allMovies = Movies.objects.all()
    # 10 veya üstü alan film / dizi trende girsin
    # lookup metodu kullan
    # lte = <= 
    # gte = >=
    # gt = >
    # lt = <
    # icontains = field içinde arama yapar
    # searchResults = allMovies.filter(movie_name__icontains="Q")
    # movies["Arama Sonuçları"] = searchResults

    trends = allMovies.filter(movie_likes__gte=10)

    if trends.count():
        movies["En Çok Beğenilenler"] = trends

    # tüm türleri çek
    categories = MovieType.objects.all()
    # tüm kategorileri döngüye sok
    for category in categories:
        # category = film, dizi, çizgi-dizi

        movie = allMovies.filter(movie_type__type = category.type)

        # key/ value şeklinde gönder
        if movie.count():
            # film: [black hawk down, mad max]
            movies[category.type] = movie
    
    # tüm filmleri çeq
    context['dynamic'] = movies.items()
    # random banner
    # order_by ilgili objeyi sıralar, ? rastgele sıralamaya yarar
    context['randomBanner'] = Movies.objects.all().order_by("?").first()


    return render(request, 'dashboard.html', context)


# sadece filmler/diziler
def only_movies(request, categoryId):

    context = {}
    series = {}
        # tüm türleri çek
    categories = MovieType.objects.filter(id = categoryId).first()
    movies = Movies.objects.filter(movie_type = categories.id)

    # trend
    trends = movies.filter(movie_likes__gte=10)
    if trends.count():
        outputMsg = ""

        if categories.type == "Film":
            outputMsg = "En Çok Beğenilen Filmler"
        elif categories.type == "Dizi":
            outputMsg = "En Çok Beğenilen Diziler"

        series[outputMsg] = trends


    series[categories.type] = movies
    context["dynamic"] = series.items()

    print("veriler:", context["dynamic"])
    context['randomBanner'] = movies.order_by('?').first()
    # tüm kategorileri döngüye sok
    return render(request, "dashboard.html", context)




# profil seçme alanı
def user_profile_select(request):
    context = {}

    if request.method == 'POST':

        totalProfiles = request.user.profiles.count()

        if totalProfiles >= 5:
            # toplam profil saysı 5 den fazla oldugu icin hesap açamaz.
            return redirect('user_profile_select')
        
        new_profile = CreateProfile(request.POST, request.FILES)

        if new_profile.is_valid():
            # veritabnı akyit vs
            profileInstance = new_profile.save()
            # oluşturlan profili hesaba at
            request.user.profiles.add(profileInstance)
            # yönlendir
            return redirect('user_profile_select')
        else:
            # form hataları
            print("[user_profile_select fn]:",new_profile.errors)
            return redirect('user_profile_select')

    else:
        # profil olusturma formunu gönder
        context['profileForm'] = CreateProfile()
        print("verii:", context)
        return render(request, 'profileSelect.html', context)
    

# listem
def loadMyList(request):
    context = {}
    myList = {}

    myList['Listem'] = request.selectedProfile.list.all()
    context['dynamic'] = myList.items()

    return render(request, 'myList.html', context)