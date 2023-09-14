from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(NetflixUser)
admin.site.register(NetflixProfile)
admin.site.register(MovieCategory)
admin.site.register(MovieType)
admin.site.register(Movies)
admin.site.register(DebitCard)
admin.site.register(ResetPassword)