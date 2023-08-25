from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(NetflixUser)
admin.site.register(NetflixProfile)
admin.site.register(MovieTypes)
admin.site.register(Movies)
admin.site.register(MovieCategories)