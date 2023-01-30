from django.contrib.auth.decorators import login_required as login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView
from django.views.generic import DetailView
from authentication.models import CurrentReviewCenter
from job.forms import JobApplicationForm, JobPostForm 

from job.models import Certificate, JobApplication, JobPost, JobRequirements
from job.tables import JobPostTable
from quiz.models import Quiz

# Create your views here.

class JobListView(LoginRequiredMixin, SingleTableView,):
    model = JobPost
    table_class = JobPostTable
    template_name = 'job/job_list.html'
    # table_pagination = {
    #     'per_page': 5,
    # }
    # strict=False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        
        current = CurrentReviewCenter.objects.filter(user=self.request.user).first()

        if current is None:
            return JobPost.objects.none()

        current = CurrentReviewCenter.objects.filter(user=self.request.user).first()
        if current is not None:

            pass_certificates = Certificate.objects.filter(~Q(file=''), user=self.request.user, review_center=current.review_center).values_list('quiz', flat=True)

            pass_quizzes_id = list(pass_certificates)

            if len(pass_quizzes_id) > 0:                
                condition = Q(certificate_quiz__pk=pass_quizzes_id[0])
                for string in pass_quizzes_id[1:]:
                    condition &= Q(certificate_quiz__pk=string)
                passed_job_post = JobRequirements.objects.filter(condition).values_list('job_post', flat=True)
                
                passed_job_post_id = [i for i in list(passed_job_post) if i is not None]

                if len(passed_job_post_id) > 0:
                    job_condition = Q(pk__contains=passed_job_post_id[0])
                    for string in passed_job_post_id[1:]:
                        job_condition &= Q(pk__contains=string)
                    jobs_for_you = JobPost.objects.filter(job_condition, company__review_center=current.review_center)

                    return jobs_for_you

        return JobPost.objects.none()

class JobDetailView(LoginRequiredMixin, DetailView):
    model = JobPost
    context_object_name = 'job_post'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['form'] = JobPostForm(initial=self.object.__dict__)

        context['application_form'] = JobApplicationForm()
        return context

@login_required
def submit_job_application(request, slug):
    if request.method != 'POST':
        return HttpResponseBadRequest()


    form = JobApplicationForm(request.POST)

    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            # create a new `Band` and save it to the db
            application = form.save()
            # redirect to the detail page of the band we just created
            # we can provide the url pattern arguments as arguments to redirect function
            return redirect('job:jobpost_detail', slug=slug)

    else:
        form = JobApplicationForm()

    return redirect('job:jobpost_detail', slug=slug)