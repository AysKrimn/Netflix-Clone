from django.db import models
from django.contrib.auth.models import AbstractUser


# film tipleri
class MovieTypes(models.Model):
       # dizi, film, çizgi-dizi  
      type = models.CharField(("Tip"), max_length=50)


      def __str__(self) -> str:
            return self.type
# film/dizi kategorileri
class MovieCategories(models.Model):
      kategori_adi = models.CharField(("Alt Kategori Adı"), max_length=50)

      def __str__(self) -> str:
            return self.kategori_adi

# filmler
class Movies(models.Model):
      
      movie_name = models.CharField(("İsmi"), max_length=50)
      movie_description = models.TextField(("Açıklama"), max_length=400)
      movie_type = models.ForeignKey(MovieTypes, verbose_name=("Türü"), on_delete=models.CASCADE)
      movie_image = models.FileField(("Banner"), upload_to="Uploads", max_length=100)
      movie_likes = models.PositiveIntegerField(default=0)
      movie_categories = models.ManyToManyField(MovieCategories, verbose_name=("Etiketler"))
      movie_source = models.URLField(("Kaynak"), max_length=200, blank=True, help_text="Filmin URL'i")

      def __str__(self) -> str:
            return self.movie_name



      
class NetflixProfile(models.Model):
    # profil  
    main_account = models.ForeignKey("netflix_user_app.NetflixUser", verbose_name=("Ana Hesap"), on_delete=models.CASCADE, default=1)
    name = models.CharField(("Hesap Adı"), max_length=50)
    avatar = models.FileField(("Fotoğraf"), upload_to="Avatars", default="/static/image/avatar.png", max_length=100, blank=True)
    # dizi, film listesi
    list = models.ManyToManyField(Movies, verbose_name=("Liste"), blank=True)
    # hesaba şifre konulacak
    # fav

    
    def __str__(self) -> str:
          return self.name
    

# Create your models here.
class NetflixUser(AbstractUser):

       profile = models.ManyToManyField(NetflixProfile, verbose_name=("Alt Hesap"))
    
