from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class CustomUserAdmin(UserAdmin):
    model = NewUser
    list_display = ('username', 'last_login')
    fieldsets = UserAdmin.fieldsets + (
        ('Profil Alanı', 
         {'fields': ('avatar', 'movie_list')}),
    )

admin.site.register(NewUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Type)
# Register your models here.
