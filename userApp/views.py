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
                return redirect('browse-movies')
    else:
        # get istekleri
        return render(request, 'login.html')




# filmlerin yüklendiği sayfa
def boardIndex(request):
    return render(request, 'browse-index.html')