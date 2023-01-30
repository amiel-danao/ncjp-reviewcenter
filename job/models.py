from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from quiz.models import Quiz
from system.models import ReviewCenter

class CompanyIndustry(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    review_center = models.ForeignKey(ReviewCenter, blank=True, on_delete=models.SET_NULL, null=True, default=None)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Company Industries'

class Company(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    overview = models.CharField(max_length=1000, blank=False, default='')
    company_size = models.PositiveBigIntegerField(default=1, validators=(MinValueValidator(1),))
    industry = models.ForeignKey(CompanyIndustry, on_delete=models.SET_NULL, null=True)
    average_processing_time = models.PositiveIntegerField(default=1, validators=(MinValueValidator(0),))
    benefits_and_others = models.CharField(max_length=256, blank=False, default='')
    thumbnail = models.ImageField(upload_to='company_thumbnails/', blank=True, default='')
    logo = models.ImageField(upload_to='company_logos/', blank=False, default='')
    review_center = models.ForeignKey(ReviewCenter, blank=True, on_delete=models.SET_NULL, null=True, default=None)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class JobType(models.IntegerChoices):
    FULL_TIME = 1
    PART_TIME = 2






        





class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=False)
    file = models.FileField(upload_to='certificate/', blank=True, default='')
    date = models.DateField(auto_now_add=True)
    review_center = models.ForeignKey(ReviewCenter, blank=True, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f'{self.user.email}'




class JobPost(models.Model):
    title = models.CharField(max_length=100, blank=False, default='')
    position = models.CharField(max_length=100, blank=False, default='')
    job_description = models.CharField(max_length=256, blank=False, default='')
    
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
    slug = models.SlugField(null=False, unique=True, default='', allow_unicode=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("jobpost_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class JobRequirements(models.Model):
    certificate_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=False, default=None)
    job_post = models.ForeignKey(JobPost, on_delete=models.SET_NULL, blank=True, default=None, null=True)
    def __str__(self):
        return f'{self.certificate_quiz.title}'

    class Meta:
        verbose_name_plural = 'Job Requirements'


class ApplicationStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    FOR_INTERVIEW = 2, "For interview"
    FOR_REQUIREMENTS = 3, "For Requirements"
    HIRED = 4, "Hired"


class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    resume = models.FileField(upload_to='resumes/', blank=False, default='')
    expected_salary = models.PositiveBigIntegerField(blank=False, default=0)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=True, default=None, null=True)
    message_to_employer = models.CharField(max_length=255, default='', blank=True)
    status = models.PositiveSmallIntegerField(choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.user} - {self.job_post}'