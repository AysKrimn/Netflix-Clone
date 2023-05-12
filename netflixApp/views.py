from django.shortcuts import render, redirect

# template  dosyalarının hazırlanması
def index(request):

    if request.user.is_authenticated:
        return redirect('browse-movies')
    
    # anasayfa
    return render(request, 'index.html')
