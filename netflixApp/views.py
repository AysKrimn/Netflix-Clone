from django.shortcuts import render, redirect

# template  dosyalarının hazırlanması
def index(request):

    if request.user.is_authenticated:

            # nereden geldiyse oraya yönlendir
            previous_url = request.META.get('HTTP_REFERER')   

            if previous_url:
                  return redirect(previous_url)

            # yoksa hesap seçme kısmına yönlendir       
            return redirect('browse-profile')
    
    # anasayfa
    return render(request, 'index.html')
