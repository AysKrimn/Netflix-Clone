from django.db import models

# Create your models here.
class Personel(models.Model):

    name = models.CharField(("Adı"), max_length=50)
    lastname = models.CharField(("SoyAdı"), max_length=50)
    salary = models.IntegerField(("Maaş"), default=0)
    role = models.CharField(("Rolü"), max_length=50)


    def __str__(self) -> str:
        return self.name