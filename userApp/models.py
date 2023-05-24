from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class NetflixUser(AbstractUser):
    profile = models.ManyToManyField("userApp.NetflixProfile", verbose_name=("Userin Alt Hesapları"))



# profil kısmı
class NetflixProfile(models.Model):
    # favoriye alınan filmler/diziler
    user = models.ForeignKey("userApp.NetflixUser", verbose_name=("Ana Hesabı"), on_delete=models.CASCADE, default=1)
    name = models.CharField(("Profil Adı"), max_length=50, default="")
    movie = models.ManyToManyField("userApp.Movies", verbose_name=("Favori Listesi"), default=1)
    avatar = models.FileField(("User Avatar"), upload_to="Avatar", max_length=100, default="", blank=True, null=True)
    profile_createdAt = models.DateTimeField(("Oluşturulma Tarihi"), auto_now=True)

    def __str__(self):
       return self.name
    
    def handleAvatar(self):
       if self.avatar:
          return "/{path}".format(path=self.avatar)
       else:
          return "/static/img/smile-icon.jpg"

# kategoriler
class Categories(models.Model):
    # aksiyon, dram vs
   category = models.CharField(("Kategori"), max_length=50)

   def __str__(self) -> str:
      return self.category

# tür
class Type(models.Model):
   # film, dizi, çizgi-dizi vs   
   type = models.CharField(("İçerik Türü"), max_length=50)

   def __str__(self):
      return self.type

# film modeli
class Movies(models.Model):
  movie_title = models.CharField(("Başlık"), max_length=50)
  movie_description = models.TextField(("Açıklama"))
  movie_category = models.ManyToManyField("userApp.Categories", verbose_name=("Tags"))
  movie_type = models.ForeignKey("userApp.Type", verbose_name=("İçerik Tipi"), help_text="Film/Dizi içerik türü", on_delete=models.CASCADE)
  movie_cover = models.FileField(("Afiş"), upload_to="Uploads", max_length=100, blank=True, null=True)


  def __str__(self) -> str:
     return self.movie_title
  

  # conver döndür yoksa netflix logo
  def handleConver(self):
      if self.movie_cover:
         return self.movie_cover
      else:
         # burada statik bir no_avatar.png fotoğrafı döndür
         pass
  