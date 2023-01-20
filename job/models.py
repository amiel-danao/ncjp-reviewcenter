from django.core.validators import MinValueValidator
from django.db import models

class CompanyIndustry(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'CompanyIndustries'

class Company(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    overview = models.CharField(max_length=1000, blank=False, default='')
    company_size = models.PositiveBigIntegerField(default=1, validators=(MinValueValidator(1),))
    industry = models.ForeignKey(CompanyIndustry, on_delete=models.SET_NULL, null=True)
    average_processing_time = models.PositiveIntegerField(default=1, validators=(MinValueValidator(0),))
    benefits_and_others = models.CharField(max_length=256, blank=False, default='')
    thumbnail = models.ImageField(upload_to='company_thumbnails/', blank=True, default='')
    logo = models.ImageField(upload_to='company_logos/', blank=True, default='')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class JobType(models.IntegerChoices):
    FULL_TIME = 1
    PART_TIME = 2


class JobPost(models.Model):
    title = models.CharField(max_length=100, blank=False, default='')
    position = models.CharField(max_length=100, blank=False, default='')
    job_description = models.CharField(max_length=256, blank=False, default='')
    job_requirements = models.CharField(max_length=259, blank=False, default='')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    job_type = models.PositiveSmallIntegerField(
        choices=JobType.choices,
        default=JobType.FULL_TIME
    )
    career_level = models.CharField(max_length=60, blank=False, default='')
    years_of_experience = models.PositiveIntegerField(default=1, validators=(MinValueValidator(1),))
    address = models.CharField(max_length=100, default='', blank= False)
    salary_range = models.CharField(max_length=50, default='', blank=True)

    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title