from django.forms import Field
from django import forms

from job.models import JobApplication, JobPost

class JobPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobPostForm, self).__init__(*args, **kwargs)
        # instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['disabled'] = True


    class Meta:
        model = JobPost
        exclude = ('slug',)

class JobApplicationForm(forms.ModelForm):

    message_to_employer = forms.CharField(widget=forms.Textarea(),required=False)

    class Meta:
        model = JobApplication
        exclude = ('user', 'job_post', 'status')