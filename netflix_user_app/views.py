from django.shortcuts import render, redirect

# auth
from django.contrib.auth import authenticate, login, logout
# user model
from .models import *
from .form import *

# flash message
from django.contrib import messages
# decorator
from django.contrib.auth.decorators import login_required


from random import randint

# rastgele name olusturan fn
def generateRandomUserName(username):

        newName = username + str(randint(1000, 9000))
        return newName
# Create your views here.
def user_login(request):


    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username = username, password = password)

            if user is None:
                # böyle bir user yok
                messages.error(request, "Kullanıcı adı veya şifre yanlış")
                return redirect('user-login')
            
            else:
                login(request, user)
                # dahsboarda yönlendir
                return redirect('user-profile-select')
        else:
            # username veya password verilmedi
            pass
    
    else:
        return render(request, 'login.html')




def user_register(request):

    if request.method == 'POST':
        
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if email and username and password:
            # böyle bir mail var mı?
            registeredEmail = NetflixUser.objects.filter(email = email).exists()
          

            if registeredEmail:
                # kullanıcı bulundu hata döndür
                messages.error(request, "Böyle bir email adresine sahip kullanıcı mevcut")
                return redirect('user-register')
         
            registeredUsername = NetflixUser.objects.filter(username = username).exists()

            if registeredUsername:

                username = generateRandomUserName(username)

            # veritabanına kayıtet
            account = NetflixUser.objects.create(email = email, username = username)
            account.set_password(password)
            account.save()

            messages.success(request, "Başarılı bir şekilde hesabınız {hesapAdi} olarak oluştu lütfen giriş yapınız.".format(hesapAdi = username))
            return redirect('user-login')


    
    else:
        return render(request, 'register.html')
    

# çıkış
def user_logout(request):
    
    if request.user.is_authenticated:

        logout(request)
        return redirect('homepage')
     
    else:
        return redirect('user-login')


# profile select kısmı
def user_profile_select(request):
    context = {}

    if request.method == 'POST':
        
        form = CreateProfile(request.POST, request.FILES)

        if form.is_valid():

            new_profile = form.save(commit=False)
            new_profile.main_account = request.user
            # şimdi kaydet
            new_profile.save()
            #  usere bu hesabı ata
            request.user.profile.add(new_profile)
            return redirect('user-profile-select')
        
        else:
            # bisiler ters gitti
            print("form errors:", form.errors)
            return redirect('user-profile-select')


    else:
        context['form'] = CreateProfile()
        return render(request, 'profileSelect.html', context)
    

# dashboard
@login_required(login_url="user-login")
def user_dashboard(request, profileId):
    context = {}

    selectedProfile = NetflixProfile.objects.filter(id=profileId).first()
    context['profile'] = selectedProfile

    movies = {}

    types = MovieTypes.objects.all()

    for tur in types:

        movie = Movies.objects.filter(movie_type = tur)
        movies[tur] = movie
    else:
        context["ogeler"] = movies.items()


    # rastgele source
    randomMovie = Movies.objects.all().order_by("?").first()
    context["random"] = randomMovie

    print("bulunan filmler:", movies)
    return render(request, 'dashboard.html', context)