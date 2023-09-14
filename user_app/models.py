from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser

import random, string
# Create your models here.


# netflix profile
class NetflixProfile(models.Model):

    avatar = models.ImageField(("Avatar"), upload_to="Avatars", default="static/img/smile-icon.jpg", max_length=None)
    name = models.CharField(("Hesap Adı"), max_length=50)
    list = models.ManyToManyField("user_app.Movies", verbose_name=("Film/Dizi Listesi"), blank=True)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
# netflix user
class NetflixUser(AbstractUser):
    # userin yan hesapları
    profiles = models.ManyToManyField(NetflixProfile, verbose_name=("Yan Hesaplar"))
    tel = models.CharField(("Telefon Numarası"), max_length=50, blank=True)
    is_premiumUser = models.BooleanField(("Abone mi"), default=False)
    kidProtect = models.BooleanField(("Ebeveyn Koruması"), default=False)

    def __str__(self) -> str:
        return self.username

# film türü
class MovieType(models.Model):
    # örneğin: dizi, film, animasyon, çizgi-dizi vs
    type = models.CharField(("Tür"), max_length=50)

    def __str__(self) -> str:
        return self.type

# film kategorisi
class MovieCategory(models.Model):
    name = models.CharField(("Kategori"), max_length=50)

    def __str__(self) -> str:
        return self.name

# film modelleri
class Movies(models.Model):

    movie_name = models.CharField(("Film Adı"), max_length=50)
    movie_type = models.ForeignKey(MovieType, verbose_name=("Türü"), on_delete=models.CASCADE)
    movie_description = models.TextField(("Açıklama"), max_length=350)
    movie_banner = models.ImageField(("Banner"), upload_to="Banners", max_length=None)
    movie_category = models.ManyToManyField(MovieCategory, verbose_name=("Kategoriler"))
    movie_likes = models.PositiveIntegerField(("Beğeni Sayısı"), default=0)
    movie_source = models.FileField(("Source"), upload_to="Movies", max_length=100)
    movie_createdAt = models.DateTimeField(auto_now=True)
    movie_recommended_age = models.PositiveIntegerField(("Yaş Aralığı"), default=15)

    def __str__(self):
        return self.movie_name


    def similar_movies(self):
        data = {}
        # ilgili filmin kategorilerini çek ve querysete kendisini dahil etme
        movies = Movies.objects.filter(movie_category__in = self.movie_category.all()).exclude(id = self.id)
        
        # movies filter oldugu icin bir array geliyor verilerin hepsine tek tek ulas
        for movie in movies:
            # eğer items içinde movienin idsi yoksa bunu kayit ettir (aynı verilerin tekrar tekrar gelmemesi icin)
            if not movie.id in data:
                data[movie.id] = movie
                
        return data.items()
    
    def handleCategories(self):
        data = []
        categories = self.movie_category.all()
        
        for category in categories:
            data.append(category.name)

        return ", ".join(data)
    

from django.core.validators import MinLengthValidator, MinValueValidator

class DebitCard(models.Model):
    
    account = models.ForeignKey(NetflixUser, verbose_name=("Kayıtlı"), on_delete=models.CASCADE)
    name = models.CharField(("İsim Soyisim"), max_length=50)
    cardName = models.CharField(("Karttaki Ad/Soyad"), max_length=50)
    email = models.CharField(("E-mail"), max_length=50)
    adress = models.TextField(("Adres"))
    zip = models.PositiveIntegerField(("Zip Kod"))
    debitNo = models.PositiveIntegerField(("Kredi Kart Numarısı"))
    expiredMonth = models.PositiveIntegerField(("Ay"), validators=[MinValueValidator(2)])
    expiredYear = models.PositiveIntegerField(("Yıl"))
    cvv = models.PositiveIntegerField(("Güvenlik kod"))

    def __str__(self) -> str:
        return self.account.username
    

def generateRandomId():
    length = 45
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# user şifresini sıfırlayacağı zaman biz bir ticket açıcaz
class ResetPassword(models.Model):
    user = models.ForeignKey(NetflixUser, verbose_name=("Hesap"), on_delete=models.CASCADE)
    tickedId = models.CharField(("Ticket"), max_length=50, default=generateRandomId, unique=True)


    def __str__(self) -> str:
        return "{} id: {}".format(self.user.username, self.tickedId)