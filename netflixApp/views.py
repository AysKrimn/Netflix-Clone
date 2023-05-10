from django.shortcuts import render

# template  dosyalarının hazırlanması
def index(request):

    return render(request, 'index.html')
