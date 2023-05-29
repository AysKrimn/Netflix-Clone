from django.shortcuts import render, redirect

# template  dosyalarının hazırlanması
def index(request):

    if request.user.is_authenticated:

            profileId = request.GET.get('watch')
            
            if profileId:

                  return redirect('browse-movies', profileId=profileId)
            else:
                  # hesap kısmına yönlendir
                  return redirect("browse-profile")
    
    # anasayfa
    return render(request, 'index.html')
