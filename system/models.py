from django_extensions.db.fields import AutoSlugField
from  embed_video.fields  import  EmbedVideoField
import re
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings



class NCChoices(models.IntegerChoices):
    NC1 = 1, "NC1"
    NC2 = 2, "NC2"
    NC3 = 3, "NC3"
    NC4 = 4, "NC4"


class ReviewCenter(models.Model):
    name = models.CharField(max_length=256, blank=False, default='')
    thumbnail = models.ImageField(upload_to='reviewcenters/', blank=False)
    description = models.CharField(max_length=256, blank=False, default='')
    slug = models.SlugField(max_length=255, null=False, unique=True, default='', allow_unicode=True)
    active = models.BooleanField(default=True)

    def __str__(self):
       return self.name
       
    def get_absolute_url(self):
        return reverse("reviewcenter_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=60, blank=False, default='', unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class CourseManager(models.Manager):
    pass
    # def new_category(self, name):
    #     new_category = self.create(category=re.sub('\s+', '-', name)
    #                                .lower())

    #     new_category.save()
    #     return new_category


class Course(models.Model):    
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60, blank=False, default='', unique=True)
    abbreviation = models.CharField(max_length=16, blank=False, null=False, default='')
    thumbnail = models.ImageField(upload_to='courses/', blank=False, null=True, )
    description = models.CharField(max_length=255, blank=True)
    nc_level = models.PositiveIntegerField(default=NCChoices.NC1, choices=NCChoices.choices)
    major = models.CharField(max_length=60, blank=True, default='')
    review_center = models.ForeignKey(ReviewCenter, blank=True, on_delete=models.SET_NULL, null=True, )

    category = models.SlugField(
        verbose_name=_("Category"),
        default='',
        max_length=255,
        unique=True, allow_unicode=True)

    objects = CourseManager()

    def save(self, *args, **kwargs):  # new
        self.category = slugify(self.name)
        return super().save(*args, **kwargs)


    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0, validators=(MinValueValidator(0),))
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    # first_name = models.CharField(blank=False, default='', max_length=50)
    # middle_name = models.CharField(blank=True, max_length=50)
    # last_name = models.CharField(blank=False, max_length=50, default='')
    # address = models.CharField(blank=False, max_length=50, default='')
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, )
    student = models.ForeignKey(to='authentication.Student', on_delete=models.SET_NULL, null=True, )

    def __str__(self):
        return f'{self.user}, {self.course}, {self.review_center}'


    class Meta:
        verbose_name = 'Payment Information'


class CoursePrice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0, validators=(MinValueValidator(0),))
    previous_price = models.FloatField(default=0, validators=(MinValueValidator(0),))
    active = models.BooleanField(default=True)
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, )

    def __str__(self):
        return self.course.name


class Video(models.Model):
    title = models.CharField(max_length=100, blank=False, default='')
    description = models.CharField(max_length=1000, blank=False, default='')
    # thumbnail = models.ImageField(upload_to='video_thumbnails/', default=f'img/default_video_thumbnail.png', blank=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    url = EmbedVideoField()
    date_posted = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, default='', unique=True, allow_unicode=True)
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, )

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class VideoComment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.CharField(max_length=400, blank=False, default='Anonymous comment')
    date_posted = models.DateTimeField(auto_now_add=True)
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, )

    def __str__(self):
        return f'{str(self.video)}, {self.sender}, {self.text[:20]}, {self.date_posted}'

class ReviewCourse(models.Model):
    title = models.CharField(max_length=120, blank=False, default='')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, )

    def __str__(self):
        return self.title

class ReviewMaterial(models.Model):
    review_course = models.ForeignKey(ReviewCourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False, default='')
    content = models.CharField(max_length=1024, blank=True, default='')
    image = models.ImageField(upload_to='review_materials/', blank=False)
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, )

    def __str__(self):
        return self.title


