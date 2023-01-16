from django.db import models


    
class Student(models.Model):
    school_id = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=False, default='')
    first_name = models.CharField(blank=False, default='', max_length=50)
    middle_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.school_id