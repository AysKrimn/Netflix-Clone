from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    # eğer kullanıcı giriş yapmışsa bunu film-seçme ekranına gönder
    if request.user.is_authenticated:
        return redirect('browse')
    
    # aksi taktirde anasayfayı göster
    return render(request, 'index.html')