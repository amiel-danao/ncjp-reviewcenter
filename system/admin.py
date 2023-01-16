from django.contrib import admin
from authentication.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.site_header = "NCST Review Center"
admin.site.site_title = "Review Center Admin"
admin.site.index_title = "Welcome to Admin's Panel"