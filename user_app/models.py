from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.movie_name
