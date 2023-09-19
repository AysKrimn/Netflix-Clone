from django.contrib import admin

from .models import *

# admin sayfası custom
admin.site.site_header = "Neos Admin Panel"
admin.site.site_title = "Neos Panel"
admin.site.index_title = "Neos Yönetimi"
# admin.site.site_url = "/browse"
# netflix profiles
class ProfileView(admin.ModelAdmin):

    list_display = ('name', "createdAt", 'id')
    list_filter = ('name',)
    search_fields = ('name',)
    list_display_links = ('createdAt', 'id')
    list_editable = ["name"]

class UserViews(admin.ModelAdmin):
    list_display = ('username', "date_joined", "kidProtect", 'is_premiumUser')
    ordering = ('date_joined',)
    list_filter = ("is_premiumUser", 'kidProtect')
    date_hierarchy = ('date_joined')
    actions = ('handle_kid_protection',)


    def handle_kid_protection(self, request, queryset):
        
        status = queryset.filter().first()
        print("durum:", status.kidProtect)
        
        if status.kidProtect == True:
            update_count = queryset.update(kidProtect=False)
            self.message_user(request, "({}) Başarılı bir şekilde ebeveyn koruması kaldırıldı.".format(update_count))
        else:
            update_count = queryset.update(kidProtect=True)
            self.message_user(request, "({}) Başarılı bir şekilde ebeveyn koruması etkinleştirildi.".format(update_count))

    handle_kid_protection.short_description = "Ebeveyn korumasını düzenle"

# Register your models here.
admin.site.register(NetflixUser, UserViews)
admin.site.register(NetflixProfile, ProfileView)
admin.site.register(MovieCategory)
admin.site.register(MovieType)
admin.site.register(Movies)
admin.site.register(DebitCard)
admin.site.register(ResetPassword)