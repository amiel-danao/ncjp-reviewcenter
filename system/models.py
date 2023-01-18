from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
    
class Student(models.Model):
    school_id = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=False, default='')
    first_name = models.CharField(blank=False, default='', max_length=50)
    middle_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.school_id


class ReviewCenter(models.Model):
    name = models.CharField(max_length=256, blank=False, default='')
    thumbnail = models.ImageField(upload_to='reviewcenters/', blank=False)
    description = models.CharField(max_length=256, blank=False, default='')
    slug = models.SlugField(max_length=255, null=False, unique=True, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
       return self.name
       
    def get_absolute_url(self):
        return reverse("reviewcenter_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=60, blank=False, default='', unique=True)
    description = models.CharField(max_length=255, blank=True)


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60, blank=False, default='', unique=True)
    description = models.CharField(max_length=255, blank=True)
    level = models.PositiveIntegerField(default=1, validators=(MinValueValidator(1), ))
    major = models.CharField(max_length=60, blank=True, default='')