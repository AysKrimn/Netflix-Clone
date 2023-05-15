from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
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
        return render(request, 'login.html')


# hesapların seçildiği alan
def browseProfile(request):
    return render(request, 'browseProfile.html')


# filmlerin yüklendiği sayfa
def boardIndex(request):
    return render(request, 'browse-index.html')



# user çıkış yapmışsa
def user_logout(request):

    if request.user.is_authenticated:
        logout(request)
        return redirect('anasayfa')
    
    else:
        return redirect('user_login')