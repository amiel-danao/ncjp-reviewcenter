from django.contrib import admin
from django import forms
from job.models import Company, CompanyIndustry, JobPost

# Register your models here.
@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'position', 'salary_range', 'date_posted')
    exclude = ('slug', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(JobPostAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        textarea_fields = ('job_requirements', 'job_description', 'address')
        if db_field.name in textarea_fields:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(CompanyAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        textarea_fields = ('overview', 'benefits_and_others')
        if db_field.name in textarea_fields:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


@admin.register(CompanyIndustry)
class CompanyIndustryAdmin(admin.ModelAdmin):
    pass