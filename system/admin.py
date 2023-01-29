from django.forms.models import BaseInlineFormSet
from django.contrib import admin
from authentication.models import CustomUser, Student
from system.models import CoursePrice, Department, Payment, ReviewCenter, ReviewCourse, ReviewMaterial, Video, VideoComment
from django.contrib.auth.models import Group
from  embed_video.admin  import  AdminVideoMixin
from django import forms
from paypal.standard.ipn.models import PayPalIPN

admin.site.unregister((PayPalIPN, ))

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import CustomUser
from system.models import ReviewCenter
# from authentication.models import ReviewCenterAccount

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


from django.db.models.signals import pre_save


@receiver(post_save, sender=CustomUser)
def basic_admin_changes(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.email != 'admin69@email.com':
                if instance.review_center:
                    instance.is_staff = True
                    instance.is_superuser = False
                    instance.is_active = True
                    instance.groups.add(Group.objects.get(name='ReviewCenter'))
                # else:
                #     instance.is_staff = True
                #     instance.is_superuser = False
                #     instance.is_active = True
                #     instance.groups.add(Group.objects.get(name='BasicAdmin'))
        except Exception as e:
            print(e)



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    search_fields = ('email', )
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    # fields = ('email', 'is_staff', 'is_active', 'is_review_center', 'date_joined', 'password')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ()
    fieldsets = (
        (_("Info"), {"fields": ("email", "is_active", "last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "review_center"),
            },
        ),
    )


@receiver(post_save, sender=CustomUser)
def student_account_changes(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.email != 'admin69@email.com':
                instance.is_superuser = False
                # instance.is_active = True
                instance.is_staff = False
                # instance.groups.add(Group.objects.get(name='BasicAdmin'))
        except Exception as e:
            print(e)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewCenter)
class ReviewCenterAdmin(admin.ModelAdmin):
    exclude = ('slug', )
    # prepopulated_fields = {"slug": ("name",)}
    def save_model(self, request, obj, form, change,):
        obj.created_by = request.user

        super().save_model(request, obj, form, change)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(CoursePrice)
class CoursePriceAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'price', 'previous_price', 'active')
    exclude = ('review_center', )

    def course_name(self, obj):
        return obj.course.name

    def save_model(self, request, obj, form, change,):
        if request.user.review_center:
            obj.review_center = request.user.review_center

        super().save_model(request, obj, form, change)
    
    def queryset(self, request):
        qs = super(CoursePriceAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)


@admin.register(Video)
class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    exclude = ('slug', 'review_center')

    def save_model(self, request, obj, form, change,):
        if request.user.review_center:
            obj.review_center = request.user.review_center

        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(VideoAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    def queryset(self, request):
        qs = super(VideoAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    readonly_fields = ('video', 'sender', 'text')
    exclude = ('review_center',)

    def has_add_permission(self, request):
        return False

    def queryset(self, request):
        qs = super(VideoCommentAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'course', 'price', 'review_center', 'payment_date',)
    readonly_fields = ('review_center', 'payment_date')
    fields = ('user', 'course','price', 'review_center', 'payment_date', 'first_name', 'middle_name', 'last_name', 'address' ,)

    def first_name(self, obj):
        return obj.student.first_name if obj.student.first_name else ''
    def middle_name(self, obj):
        return obj.student.middle_name if obj.student.middle_name else ''
    def last_name(self, obj):
        return obj.student.last_name if obj.student.last_name else ''

    def address(self, obj):
        return obj.student.address if obj.student.address else ''

    inline_reverse = [
                      ('student', {'fields': ['first_name', 'middle_name', 'last_name', 'address']}),
                      ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def queryset(self, request):
        qs = super(PaymentAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

class ReviewMaterialInline(admin.TabularInline):
    model = ReviewMaterial


    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ReviewMaterialInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

@admin.register(ReviewCourse)
class ReviewCourseAdmin(admin.ModelAdmin):
    inlines = [ReviewMaterialInline,]
    exclude = ('review_center',)

    def queryset(self, request):
        qs = super(ReviewCourseAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

admin.site.site_header = "NCST Review Center"
admin.site.site_title = "Review Center Admin"
admin.site.index_title = "Welcome to Admin's Panel"