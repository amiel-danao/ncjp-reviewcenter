from django.contrib import admin
from authentication.models import CustomUser
from system.models import CoursePrice, Department, ReviewCenter, Video, VideoComment
from django.contrib.auth.models import Group
from  embed_video.admin  import  AdminVideoMixin
from django import forms

admin.site.unregister(Group)

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(CoursePrice)
class CoursePriceAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'price', 'previous_price', 'active')

    def course_name(self, obj):
        return obj.course.name



@admin.register(Video)
class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(VideoAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    readonly_fields = ('video', 'sender', 'text')

    def has_add_permission(self, request):
        return False


@admin.register(ReviewCenter)
class ReviewCenterAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.site_header = "NCST Review Center"
admin.site.site_title = "Review Center Admin"
admin.site.index_title = "Welcome to Admin's Panel"