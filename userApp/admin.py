from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(NetflixUser)
admin.site.register(Categories)
admin.site.register(Type)
admin.site.register(Movies)