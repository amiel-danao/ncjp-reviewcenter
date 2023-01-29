from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from job.models import Company, JobPost
from quiz.models import Quiz
from reviewcenter.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

from system.models import Course, ReviewCenter, ReviewMaterial, Video

class RelationChoices(models.IntegerChoices):
    FATHER_MOTHER = 1, "Father/Mother"
    HUSBAND_WIFE_PARTNER = 2, "Husband/Wife/Partner"
    UNCLE_AUNT = 3, "Uncle/Aunt"
    GRANDFATHER_GRANDMOTHER = 4, "Grandmother/Grandfather"
    GUARDIAN = 5, "Guardian"
    OTHERS = 6, "Others"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(blank=False, unique=True, default='')
    email = models.EmailField(_("email address"), unique=True)
    picture = models.ImageField(
        upload_to='images/', blank=True, null=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, default=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def username(self):
        return self.email

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"


class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, default=None)
    first_name = models.CharField(blank=False, default='', max_length=50)
    middle_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=False, max_length=50, default='')
    school = models.CharField(blank=False, max_length=50, default='')
    date_of_graduation = models.DateField(null=True, blank=True)
    deans_name = models.CharField(blank=False, max_length=50, default='')
    address = models.CharField(blank=False, max_length=50, default='')
    contact_person_number = models.CharField(blank=False, max_length=11, default='')
    contact_person_name = models.CharField(blank=False, max_length=50, default='')
    contact_person_relation = models.IntegerField(choices=RelationChoices.choices, default=RelationChoices.FATHER_MOTHER)


    class Meta:
        verbose_name = 'Student Profile'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class StudentProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, default=None)
    review_center = models.ForeignKey(ReviewCenter, on_delete=models.SET_NULL, null=True, default=None)
    # profile = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, default=None)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, default=None)
    review_video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, default=None)
    review_material = models.ForeignKey(ReviewMaterial, on_delete=models.SET_NULL, null=True, default=None)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, default=None)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, default=None)
    job = models.ForeignKey(JobPost, on_delete=models.SET_NULL, null=True, default=None)

