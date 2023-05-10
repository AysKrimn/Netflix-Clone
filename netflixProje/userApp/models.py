from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class NewUser(AbstractUser):
    avatar = models.FileField(("Avatar"), upload_to="Avatar", max_length=100, blank=True, null=True)
    movie_list = models.ManyToManyField("userApp.Movie", verbose_name=("Favori Listesi"))


    def use_avatar_or_default(self):
        if self.avatar:
            return self.avatar
        else:
            # varsayılan bir avatar döndür.
            return "/img/film1.jpg"


# Kategoriler
class Category(models.Model):
    category_name = models.CharField(("Kategori İsmi"), max_length=50)

    def __str__(self):
        return self.category_name
    

class Type(models.Model):
    movie_type = models.CharField(("İçerik Türü"), max_length=50)

    def __str__(self):
        return self.movie_type

# film/dizi classi
class Movie(models.Model):
    movie_name = models.CharField(("Film Adı"), max_length=50)
    movie_description = models.TextField(("Film Açıklaması"), max_length=250)
    movie_avatar = models.FileField(("Banner"), upload_to="Uploads", max_length=100)
    movie_createdAt = models.TimeField(("Eklenme Tarihi"), auto_now=True)
    movie_category = models.ManyToManyField(Category, verbose_name=("Kategorisi"))
    movie_type = models.ForeignKey(Type, verbose_name=("İçerik Türü"), default="Dizi", on_delete=models.CASCADE)
    movie_liked = models.PositiveIntegerField(("Beğeni Sayısı"), default=0)
    movie_disliked = models.PositiveIntegerField(("Beğenilmeme Sayısı"), default=0)
    


    def __str__(self):
        return self.movie_name
    


