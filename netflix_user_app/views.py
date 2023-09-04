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

        response = redirect('homepage')
        # cookiyi sil
        response.delete_cookie('selected_profile_id')
        # request cookisini sil 
        logout(request)
        # yönlendir
        return response
     
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
def user_dashboard(request):

    context = {}
    # cookie var mı? 
    profileId = request.COOKIES.get('selected_profile_id')
    print("PROFİLE:", profileId)

    # ençok like alan filmler (lookups kullan)
    #  gte = greater than equal >= 
    #  lte = less than equal <=
    # gt = >
    # ls = <
    mostLiked = Movies.objects.filter(movie_likes__gte=10)

    movies = {}

    movies["En Çok Beğenilenler"] = mostLiked

    types = MovieTypes.objects.all()

    for tur in types:

        movie = Movies.objects.filter(movie_type = tur)
        movies[tur] = movie
    else:
        context["ogeler"] = movies.items()

    
    print("movies objesi:", movies)


    # rastgele source
    randomMovie = Movies.objects.all().order_by("?").first()
    context["randomBanner"] = randomMovie

    print("bulunan filmler:", movies)
    return render(request, 'dashboard.html', context)


# kategoriye göre sırala
# sadece filmler
def only_film_or_shows(request, categoryId):
    print("userlist request:", request.profile)
    context = {}

    # ilgili kategoriyi yakala
    types = MovieTypes.objects.filter(id = categoryId)

    movies = {}

    for tur in types:

        movie = Movies.objects.filter(movie_type = tur)
        movies[tur] = movie
    else:
        context["ogeler"] = movies.items()

    # random banner
    randomMovie = Movies.objects.filter(movie_type__id = categoryId).order_by("?").first()
    context["randomBanner"] = randomMovie
        
    return render(request, 'dashboard.html', context)




# user-list
def userList(request, profileId):

    context = {}

    context['movies'] = request.profile.list.all() 

    print("data:",request.profile.list.all())

    return render(request, 'user_list.html', context)

# ayarlar
def user_account(request, userId):
    context = {}
    
    return render(request, "account.html", context)


# sadece user_accounttan gelen post isteklerini al
@login_required(login_url='user-login')
def change_user_setting(request):

    user = NetflixUser.objects.filter(id = request.user.id).first()

    if request.method == 'POST':
        
        # nitelikleri al
        email = request.POST.get('email')
        tel = request.POST.get('telno')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('new_password')
        newPassword_2 = request.POST.get('new_password_again')

        if email:
            user.email = email

        if tel:
            user.tel = tel

        if oldPassword and newPassword and newPassword_2:
            # eski şifre şuanki şifre ile uyuşuyor mu?
            match = user.check_password(oldPassword)
            # eğer match true dönerse yeni şifreleri kontrol et
            if match:
                if newPassword == newPassword_2:
                    # yeni şifreyi oluştur
                    user.set_password(newPassword)
                else:
                    # yeni şifreler uyuşmuyor
                    print("yeni şifreler uyuşmuyor")
                    pass
            else:
                # eski şifre uyusmuyor
                print("eski şifre uyuşmuyor")
                pass
        # değişikleri kaydet
        user.save()
        # yönlendir
        return redirect('change-user-setting')

    else:

        previusLink = request.META.get("HTTP_REFERER")
        print("linklerr:", previusLink)

        if previusLink:
            return redirect(previusLink)
        else:
            return redirect("user-account", request.user.id)
        

# kart bilgilerini al
@login_required(login_url='user-login')
def get_or_setCard(request):

    user = NetflixUser.objects.filter(id = request.user.id).first()

    if request.method == 'POST':
        
        name = request.POST.get('cardName')
        adress = request.POST.get('cardAdress')
        city = request.POST.get('cardCity')
        zip = request.POST.get('cardZip')
        cardNo = request.POST.get('cardNo')
        cardMoth = request.POST.get('expmonth')
        cardYear = request.POST.get('expyear')
        cardCVV = request.POST.get('cardCVV')
        format = "{ay}/{yıl}".format(ay = cardMoth, yıl = cardYear)
        if name and adress and city and zip and cardNo and cardMoth and cardYear and cardCVV:

            paymentCard = Card.objects.create(
                name = name,
                no = cardNo,
                cvc = cardCVV,
                adress = adress,
                city = city,
                zip = zip, 
                valid = format
            )

            user.debitCard = paymentCard
            user.isPremium = True
            user.save()
            # aynı sayfaya yönlendir
            return redirect('change-user-setting')
        else:
            # bilgiler eksik
            pass
    else:
        return redirect('change-user-setting')