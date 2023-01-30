import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from job.models import JobApplication, JobPost


class JobPostTable(tables.Table):
    class Meta:
        model = JobPost
        template_name = "django_tables2/bootstrap5.html"
        fields = ("title", "company", "position", "job_type", "date_posted")
        empty_text = _("No job found for this search query.")
        attrs = {'class': 'table table-hover shadow records-table'}

class JobApplicationTable(tables.Table):
    class Meta:
        model = JobApplication
        template_name = "django_tables2/bootstrap5.html"
        fields = ("job_post__title", "job_post__company", "job_post__position", "job_post__job_type", 'status')
        empty_text = _("No job found for this search query.")
        attrs = {'class': 'table table-hover shadow records-table'}
