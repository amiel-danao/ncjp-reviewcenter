from django.forms import Field
from django import forms

from job.models import JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        exclude = ('slug',)