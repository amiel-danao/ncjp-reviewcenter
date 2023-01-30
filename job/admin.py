from django.contrib import admin
from django import forms
from job.models import Certificate, Company, CompanyIndustry, JobApplication, JobPost, JobRequirements

# Register your models here.

class JobRequirementsInline(admin.TabularInline):
    model = JobRequirements



@admin.register(JobRequirements)
class JobRequirementsAdmin(admin.ModelAdmin):
    # inlines = [JobPostline, ]
    pass

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    inlines = [JobRequirementsInline, ]
    list_display = ('title', 'company', 'position', 'salary_range', 'date_posted')
    exclude = ('slug', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(JobPostAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        textarea_fields = ('job_description', 'address')
        if db_field.name in textarea_fields:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    def queryset(self, request):
        qs = super(CompanyAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(company__review_center=request.user.review_center)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    exclude = ( )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(CompanyAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        textarea_fields = ('overview', 'benefits_and_others')
        if db_field.name in textarea_fields:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    
    def queryset(self, request):
        qs = super(CompanyAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

    def save_model(self, request, obj, form, change,):
        if request.user.review_center:
            obj.review_center = request.user.review_center

        super().save_model(request, obj, form, change)


@admin.register(CompanyIndustry)
class CompanyIndustryAdmin(admin.ModelAdmin):
    exclude = ( )

    def queryset(self, request):
        qs = super(CompanyIndustryAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

    def save_model(self, request, obj, form, change,):
        if request.user.review_center:
            obj.review_center = request.user.review_center

        super().save_model(request, obj, form, change)



@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    fields = ('user', 'quiz', 'file', 'date')
    readonly_fields = ('date', )
    list_display = ('user', 'quiz', 'date')
    exclude = ( )

    def queryset(self, request):
        qs = super(CertificateAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

    def save_model(self, request, obj, form, change,):
        if request.user.review_center:
            obj.review_center = request.user.review_center

        super().save_model(request, obj, form, change)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'job_post', 'resume' ,'expected_salary', 'message_to_employer')

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request):
    #     return False

    def queryset(self, request):
        qs = super(JobApplicationAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(job_post__company__review_center=request.user.review_center)

    # def save_model(self, request, obj, form, change,):
    #     if request.user.review_center:
    #         obj.review_center = request.user.review_center

    #     super().save_model(request, obj, form, change)