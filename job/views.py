from django.contrib.auth.decorators import login_required as login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView
from django.views.generic import DetailView
from authentication.models import CurrentReviewCenter, StudentProgress
from job.forms import JobApplicationForm, JobPostForm 

from job.models import Certificate, JobApplication, JobPost, JobRequirements
from job.tables import JobApplicationTable, JobPostTable
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

        current = CurrentReviewCenter.objects.filter(user=self.request.user).first()
        if current is not None:
            progress = StudentProgress.objects.filter(user=self.request.user, review_center=current.review_center).first()
            if progress is not None:
                applications = JobApplication.objects.filter(user=self.request.user, job_post__company__review_center=current.review_center).first()

                if applications is not None:
                    job_post = applications.job_post
                    progress.job = job_post
                    progress.company = job_post.company
                    progress.save()

        return context

    def get_queryset(self):
        
        current = CurrentReviewCenter.objects.filter(user=self.request.user).first()

        if current is None:
            return JobPost.objects.none()

        current = CurrentReviewCenter.objects.filter(user=self.request.user).first()
        if current is not None:

            pass_certificates = Certificate.objects.filter(user=self.request.user, review_center=current.review_center).exclude(file__in=['',None]).values_list('quiz', flat=True)

            pass_quizzes_id = list(pass_certificates)

            if len(pass_quizzes_id) > 0:                
                # condition = Q(certificate_quiz__pk=pass_quizzes_id[0])
                # for string in pass_quizzes_id[1:]:
                #     condition &= Q(certificate_quiz__pk=string)
                # passed_job_post = JobRequirements.objects.filter(condition).values_list('job_post', flat=True)
                
                passed_job_post = JobRequirements.objects.all()
                q = Q()
                for quiz_id in pass_quizzes_id:
                    q = q | Q(certificate_quiz=quiz_id)
                passed_job_post.filter(q).values_list('job_post', flat=True)


                passed_job_post_id = [i for i in list(passed_job_post) if i is not None]

                if len(passed_job_post_id) > 0:
                    jobs_for_you = JobPost.objects.all()
                    q = Q()
                    for post_id in passed_job_post_id:
                        q = q | Q(pk=post_id.id)
                    jobs_for_you = jobs_for_you.filter(q, company__review_center=current.review_center)

                    # job_condition = Q(pk__contains=passed_job_post_id[0])
                    # for string in passed_job_post_id[1:]:
                    #     job_condition &= Q(pk__contains=string)
                    # jobs_for_you = JobPost.objects.filter(job_condition, company__review_center=current.review_center)

                    

                    return jobs_for_you

        return JobPost.objects.none()

class JobDetailView(LoginRequiredMixin, DetailView):
    model = JobPost
    context_object_name = 'job_post'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['form'] = JobPostForm(instance=self.object)

        context['applied'] = False

        job_application = JobApplication.objects.filter(user=self.request.user, job_post=self.object).first()

        if job_application is not None:
            context['applied'] = True

        context['application_form'] = JobApplicationForm()
        return context

@login_required
def submit_job_application(request, slug):
    if request.method != 'POST':
        return HttpResponseBadRequest()


    form = JobApplicationForm(request.POST)

    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # create a new `Band` and save it to the db

            application = form.save()

            application.user = request.user
            job_post = JobPost.objects.filter(slug=slug).first()
            if job_post is not None:
                application.job_post = job_post
            application.save()

            current = CurrentReviewCenter.objects.filter(user=request.user).first()
            if current is not None:
                progress = StudentProgress.objects.filter(user=request.user, review_center=current.review_center).first()
                if progress is not None:
                    progress.job = job_post
                    progress.save()

            # redirect to the detail page of the band we just created
            # we can provide the url pattern arguments as arguments to redirect function
            return redirect('job:jobpost_detail', slug=slug)

    else:
        form = JobApplicationForm()

    return redirect('job:jobpost_detail', slug=slug)


class JobApplicationListView(LoginRequiredMixin, SingleTableView,):
    model = JobApplication
    table_class = JobApplicationTable
    template_name = 'job/job_applications.html'
    # table_pagination = {
    #     'per_page': 5,
    # }
    # strict=False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_queryset(self):
        
        

        return JobApplication.objects.filter(user=self.request.user, )