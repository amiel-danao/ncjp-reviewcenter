import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from job.models import JobPost


class JobPostTable(tables.Table):
    class Meta:
        model = JobPost
        template_name = "django_tables2/bootstrap5.html"
        fields = ("title", "company", "position", "job_type", "date_posted")
        empty_text = _("No job found for this search query.")
        attrs = {'class': 'table table-hover shadow records-table'}
