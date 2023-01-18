from django.contrib import admin
from authentication.models import CustomUser
from system.models import ReviewCenter

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(ReviewCenter)
class ReviewCenterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.site_header = "NCST Review Center"
admin.site.site_title = "Review Center Admin"
admin.site.index_title = "Welcome to Admin's Panel"