from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import * 

# profil oluşturma formu
from .form import CreateProfile, CreateDebitCard

# api istekleri yapamk için
import requests

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

        if request.user.is_authenticated:
            return redirect('dashboard')
        
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
            # set_password ile veritabanına şifreyi hashlenmiş bir şekilde gönder
            user.set_password(user_password)
            user.save()

            # mail at
            try:

                user.email_user(
                subject = "Netflix'e hoşgeldiniz",
                message = f"{user.username} hesabınız başarılı bir şekilde oluşturuldu. Bizi tercih ettiğiniz için teşekkür ederiz. Hemen profil oluşturarak izlemenin keyfini çıkarın. http://127.0.0.1:8000/select/profile"
                 )
                
            except:
                pass


            # mesaj gönderilebilir
            return redirect('user_login')

    else:
        return render(request, 'register.html')
    
# şifre değişitme
def user_reset_password(request):

    if request.method == 'POST':
        
        email = request.POST.get('user_email')

        if email:
            # bu emaile sahip user var mi?
            user = NetflixUser.objects.filter(email = email).first()

            if user is None:
                # bu emaile sahip user yok
                return redirect('user_reset')
            
            else:
                # ticket oluştur
                ticket = ResetPassword.objects.create(user = user)
                user.email_user(
                    subject="Şifre Sıfırlama",
                    message="Merhaba {} parolanızı buradan sıfırlayabilirsiniz: http://127.0.0.1:8000/reset?id={}".format(user.username, ticket.tickedId)
                )

                # mesajlar gönderilebilir
                return redirect('user_reset')
 
    else:
        # paramda id var mı?
        ticketId = request.GET.get('id')

        if ticketId:
            validTicketId = ResetPassword.objects.filter(tickedId = ticketId).first()

            if validTicketId:
                # useri login et
                login(request, validTicketId.user)
                # ticketi sil
                # validTicketId.delete()
                return redirect('/YourAccount?reset-password=true')
            else:
                return redirect("user_login")



        return render(request, "reset_password.html")

# hesap ayarlari
@login_required(login_url='user_login')
def user_account_setting(request):
    context = {}

    if request.method == 'POST':

        form = CreateDebitCard(request.POST)

        data = {
            "cardNo": request.POST.get('debitNo'),
            "price": 30
        }

        print("form:", data)
        # custom api servisine istek at
        try:

            response = requests.post("http://localhost:8080/api/cards", json=data)
            if response.status_code == 200:

                server_message = response.json()

                if server_message.get('error'):
                    # hata mesajı vs
                    return redirect('user-account')
  
        except:
            pass

        # user bulunmuşsa:
        if form.is_valid():
                instance = form.save(commit=False)
                instance.account = request.user
                # premimumu aktif hale getir
                request.user.is_premiumUser = True
                request.user.save()
                # formu kaydet
                instance.save()
                # başarılı mesajı vs
                return redirect('user-account')
        else:
                print("form errors:", form.errors)
                return redirect('user-account')


    else:

        if not request.user.is_premiumUser:

            isRegisteredBefore = DebitCard.objects.filter(account__id = request.user.id).first()
            if isRegisteredBefore:
                  context['registeredBefore'] = True
                  context['form'] = CreateDebitCard(instance=isRegisteredBefore)
            else:
                  context['form'] = CreateDebitCard()
          
        # user hesap şifresini sıfırlama isteği ile mi geldi?
        option = request.GET.get('reset-password')

        if option and option == 'true':
            # db de var mı?
            isTicket = ResetPassword.objects.filter(user = request.user).first()

            if isTicket:
               context['removePreviousPassword'] = True

        return render(request, "account.html", context)

# hesap ayarlari değişitmre (modallardan gelen verielr buradan işlenir)
def change_user_setting(request):
    yonlendir = redirect('user-account')
    error = False
    user = NetflixUser.objects.filter(id = request.user.id).first()

    if user is None:
        # hata mesaji vs gönder
        return yonlendir
    

    if request.method == 'POST':
        # gelen verileri kontrol et
        email = request.POST.get('email')
        tel = request.POST.get('tel')

        isResetPassword = ResetPassword.objects.filter(user = request.user).first()

        if isResetPassword:
            # eski şifre gelmeyecek
            oldPassword = request.POST.get('newPassword')
        else:
            # eski şifre gelecek
            oldPassword = request.POST.get('oldPassword')

        if email:
            user.email = email
        elif tel: 
            user.tel = tel
        elif oldPassword:
             
             newPassword = request.POST.get('newPassword')
             newPasswordConfirm = request.POST.get('newPasswordConfirm')
             
             if newPassword and newPasswordConfirm and newPassword == newPasswordConfirm:
                 user.set_password(newPassword)

                 # ticketi sil
                 if isResetPassword:
                    isResetPassword.delete()

             else:
                 error = True
        else:
            # istenmeyen boş veri
            error = True


        if error:
            return yonlendir
        
        user.save()
        # aynı svye gönder
        return yonlendir

    else:
        return yonlendir


# filmlerin izlendigi yer
# bu endpointi koru
@login_required(login_url="user_login")
def user_dashboard(request):
    context = {}
    
    movies = {}

    allMovies = Movies.objects.all()

    for movie in allMovies:

        movie.similar_movies
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
    if request.user.kidProtect:

        trends = trends.filter(movie_recommended_age__lte=17)

    if trends.count():
        movies["En Çok Beğenilenler"] = trends

    # tüm türleri çek
    categories = MovieType.objects.all()
    # tüm kategorileri döngüye sok
    for category in categories:
        # category = film, dizi, çizgi-dizi

        movie = allMovies.filter(movie_type__type = category.type)

        # requestteki elemanın kid protecti aktifse
        if request.user.kidProtect:
            movie = movie.filter(movie_recommended_age__lte=17)

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
@login_required(login_url='user_login')
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