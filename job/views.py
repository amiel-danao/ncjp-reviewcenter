from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView
from django.views.generic import DetailView
from job.forms import JobPostForm 

from job.models import JobPost
from job.tables import JobPostTable

# Create your views here.

class JobListView(LoginRequiredMixin, SingleTableView,):
    model = JobPost
    table_class = JobPostTable
    template_name = 'job/job_list.html'
    table_pagination = {
        'per_page': 5,
    }
    strict=False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        
        qs = super().get_queryset()
        # qs = qs.filter(borrower__email=self.request.user.email)
        return qs

class JobDetailView(LoginRequiredMixin, DetailView):
    model = JobPost

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['form'] = JobPostForm() 
        return context