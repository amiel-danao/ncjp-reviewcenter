from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.views import View
from django.views.generic.edit import FormMixin, ModelFormMixin, FormView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required as login_required
from django.urls import reverse
from authentication.forms import StudentProfileForm
from authentication.models import CurrentReviewCenter, Student, StudentProgress
from system.context_processors import get_progress
from system.forms import VideoCommentForm
from system.models import Course, CoursePrice, Payment, ReviewCourse, ReviewMaterial, Video, VideoComment
from system.models import ReviewCenter
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings


class StudentOnlyMixin(object):
    def has_permissions(self):
        # Assumes that your Article model has a foreign key called `auteur`.
        # obj = self.get_object()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return False

        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(StudentOnlyMixin, self).dispatch(
            request, *args, **kwargs)

class PaidUserOnlyMixin(object):

    def has_permissions(self):
        current, _ = CurrentReviewCenter.objects.get_or_create(user=self.request.user)

        course_slug = self.request.GET.get('course', None)

        if course_slug is None:
            progress = StudentProgress.objects.filter(user=self.request.user).first()
            
            course_price = CoursePrice.objects.filter(course=progress.course, review_center=current.review_center).first()
            if course_price is None:
                return True

            existing_payment = Payment.objects.filter(user=self.request.user, course=course_price.course, review_center=current.review_center).first()
            if existing_payment is None and course_price.price > 0:
                return False
            return True

        if current is None or current.review_center is None or course_slug is None:
            return False
        
        if course_slug:
            course_price = CoursePrice.objects.filter(course__category=course_slug, review_center=current.review_center).first()

            if course_price is None:
                return True
            existing_payment = Payment.objects.filter(user=self.request.user, course=course_price.course, review_center=current.review_center).first()
            if existing_payment is None and course_price.price > 0:
                return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(PaidUserOnlyMixin, self).dispatch(
            request, *args, **kwargs)


def index(request):
    return render(request=request, template_name='index.html')

@login_required
def dashboard(request):
    context = {}
    menu = request.GET.get('menu', None)


    progress_value = get_progress(request)

    if progress_value is None:
        context['reviewcenters'] = ReviewCenter.objects.filter(active=True)
        return render(request=request, template_name='system/dashboard.html', context=context)
    last_step = progress_value['last_step']
    if last_step is None:
        context['reviewcenters'] = ReviewCenter.objects.filter(active=True)
        return render(request=request, template_name='system/dashboard.html', context=context)
    last_step_type = type(last_step)

    if last_step_type == ReviewCenter:
        return redirect('authentication:registration_redirect')
    elif last_step_type == Course:
        progress = StudentProgress.objects.filter(user=request.user).first()
        if progress is not None:
            course = progress.course
            if course is not None:
                course_slug = course.category
                return redirect('system:check_course_payment', course_slug=course_slug)

        context['reviewcenters'] = ReviewCenter.objects.filter(active=True)
        return render(request=request, template_name='system/dashboard.html', context=context)
    elif last_step_type == Student:
        return redirect('system:course_videos')
    elif last_step_type == Video:
        return redirect('system:review_courses')
    elif last_step_type == ReviewCourse:
        pass
    

    # if not menu or menu == 'reviewcenters':
    #     context['reviewcenters'] = ReviewCenter.objects.filter(active=True)
    #     context['active_link'] = 'review_centers'
    # elif menu == 'forums':
    #     context['can_add_question'] = True
    # elif menu == 'review':
    #     context['paid_course_list'] = CoursePrice.objects.filter(price__gt=0, active=True)
    #     context['free_course_list'] = CoursePrice.objects.filter(price=0, active=True)
    

    return render(request=request, template_name='system/dashboard.html', context=context)

# def create_or_create_progress_if_not_exist(request):
#     fetched, _ = StudentProgress.objects.get_or_create(user=request.user)
#     return fetched
            
        


# class CourseListView(LoginRequiredMixin, ListView):
#     model = Course

class VideoDetailView(LoginRequiredMixin, PaidUserOnlyMixin, FormMixin, DetailView):
    model = Video
    template_name = 'system/video_watch.html'
    form_class = VideoCommentForm

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)

        video = kwargs["object"]
        context['video_comments'] = VideoComment.objects.filter(video=video)
        context['related_videos'] = Video.objects.filter(course=video.course).exclude(id=video.id)
        context['form'] = VideoCommentForm(initial={'video': self.object})

        return context

    def get_success_url(self):
        return reverse('system:video_watch', kwargs={'course_slug': self.kwargs['course_slug'], 'video_slug': self.object.slug})

    def get_object(self):
        video = get_object_or_404(
            Video,
            slug=self.kwargs['video_slug'],
        )

        current = CurrentReviewCenter.objects.filter(user=self.request.user).first()
        progress = StudentProgress.objects.filter(user=self.request.user, review_center=current.review_center).first()

        if progress is None:
            raise Http404()
        progress.review_video = video
        progress.save()

        return video

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.video = self.object
        form.save()
        return super(VideoDetailView, self).form_valid(form)


@login_required
def free_video_tutorials(request):
    context = {}

    free_courses = CoursePrice.objects.filter(price=0).values('course')
    context['video_list'] = Video.objects.filter(course__in=free_courses, active=True)

    return render(request=request, template_name='system/course_videos.html', context=context)

class VideoListView(LoginRequiredMixin, PaidUserOnlyMixin, ListView):
    model = Video
    template_name = 'system/course_videos.html'

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
    
        current = CurrentReviewCenter.objects.filter(user=self.request.user).first()
        if current is not None:
            progress = StudentProgress.objects.filter(user=self.request.user, review_center=current.review_center).first()
            if progress is not None:
                course = progress.course

        if course is None:
            raise Http404()

        context['video_list'] = Video.objects.filter(course=course, active=True)
        context['course'] = course
        context['active_link'] = 'learn'

        return context

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Http404:
            current = CurrentReviewCenter.objects.filter(user=self.request.user).first()
            if current is not None:
                progress = StudentProgress.objects.filter(user=self.request.user, review_center=current.review_center).first()
                if progress is not None:
                    course = progress.course

            if course is None:
                return redirect('authentication:registration_redirect')
    
def done_review(request):
    current = CurrentReviewCenter.objects.filter(user=request.user)
    if current is None:
        return redirect('system:reviewcenter_list')
    progress = StudentProgress.objects.filter(user=request.user).first()

    if progress is None or progress.course is None:
        return redirect('system:reviewcenter_list')

    review_course = ReviewCourse.objects.filter(course=progress.course).first()
    if review_course is None:
        return redirect('system:reviewcenter_list')

    progress.review_course = review_course
    progress.save()

    return redirect('quiz:quiz_category_list_matching', category_name=progress.course.category)

            

class ReviewMaterialListView(LoginRequiredMixin, PaidUserOnlyMixin, ListView):
    model = ReviewMaterial
    template_name = 'system/review_material_list.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        progress = StudentProgress.objects.filter(user=self.request.user).first()

        if progress is None or progress.course is None:
            return context


        review_course = ReviewCourse.objects.filter(course=progress.course).first()
        if review_course is None:
            return context

        

        content_list = ReviewMaterial.objects.filter(review_course=review_course)
        paginator = Paginator(content_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            review_material_list = paginator.page(page)
        except PageNotAnInteger:
            review_material_list = paginator.page(1)
        except EmptyPage:
            review_material_list = paginator.page(paginator.num_pages)
        
        context['is_paginated'] = True
        context['review_course'] = review_course
        context['content_list'] = content_list
        context['review_material_list'] = review_material_list
        return context

class ReviewCourseListView(LoginRequiredMixin, PaidUserOnlyMixin, ListView):
    model = ReviewCourse
    template_name = 'system/review_course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs.get('course_slug', None)
        if course_slug is None:
            return context
        course = get_object_or_404(Course, category=course_slug)
        review_course_list = ReviewCourse.objects.filter(course=course)
            
        context['course'] = course
        context['review_course_list'] = review_course_list
        return context

@login_required
def reviewcenter_list(request):
    context = {}
    context['reviewcenters'] = ReviewCenter.objects.filter(active=True)
    

    return render(request=request, template_name='system/dashboard.html', context=context)


@login_required
def reviewcenter_detail(request, slug):
    instance = ReviewCenter.objects.filter(slug__iexact = slug)
    if instance.exists():
        instance = instance.first()
        current, _ = CurrentReviewCenter.objects.get_or_create(user=request.user)
        current.review_center = instance
        current.save()

        progress, created = StudentProgress.objects.get_or_create(user=request.user, review_center=instance)
        progress.review_center = instance
        progress.save()
    else:
        return HttpResponse('<h1>Review Center Not Found</h1>')
    context = {
        'reviewcenter': instance
    }
    context['course_list'] = Course.objects.filter(review_center=instance)

    return render(request, 'system/reviewcenter_detail.html', context)

@login_required
def check_course_payment(request, course_slug):
    course = Course.objects.filter(category=course_slug).first()

    if course is None:
        current = CurrentReviewCenter.objects.filter(user=request.user).first()
        progress = StudentProgress.objects.filter(review_center=current)

        if progress is None:
            return redirect('system:reviewcenter_list')

        course = progress.course
        if course is None:
            return redirect('authentication:registration_redirect')

    existing_payment = Payment.objects.filter(user=request.user, course=course).first()

    next_url = request.GET.get('next', None)

    if existing_payment is None:
        if next_url is None:
            return redirect('system:process_payment', course_slug)
        
        response = redirect('system:process_payment', course_slug)
        response['Location'] += f'?next={next_url}'
        return response        
    else:
        if next_url is None:
            return redirect(f'system:course_videos', course_slug=course_slug)
        else:            
            if course_slug:
                return redirect(f'system:{next_url}', course_slug=course_slug)
            else:
                return redirect(f'system:{next_url}')


class PaymentView(LoginRequiredMixin, CreateView):
    model = Payment

def process_payment(request, course_slug):
    course = get_object_or_404(Course, category=course_slug)
    context = {}
    course_price = CoursePrice.objects.get(course=course)
    context['amount'] = course_price.price
    host = request.get_host()

    price = format(course_price.price, '.2f')

    done_url = reverse('system:payment_done', kwargs={'course_slug': course_slug})

    current = CurrentReviewCenter.objects.filter(user=request.user).first()
    if current is None:
        return redirect('system:reviewcenter_list')


    next_url = request.GET.get('next', None)
    if next_url:
        done_url = f"%s?next={next_url}" % reverse('system:payment_done', kwargs={'course_slug': course_slug})

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(price),
        'item_name': course.name,
        'invoice': f'{str(course.id)}-{str(request.user.email)}-{str(current.review_center.name)}',
        'currency_code': 'PHP',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, done_url),
        'cancel_return': 'http://{}{}'.format(host, reverse('system:dashboard')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'system/process_payment.html', {'course': course, 'form': form})


@csrf_exempt
def payment_done(request, course_slug):
    course = get_object_or_404(Course, category=course_slug)
    course_price = get_object_or_404(CoursePrice, course=course)
    progress = StudentProgress.objects.filter(user=request.user).first()
    review_center = progress.review_center
    student = Student.objects.filter(user=request.user).first()
    Payment.objects.get_or_create(user=request.user, price=course_price.price, course=course, review_center=review_center, student=student)
    next_url = request.GET.get('next', None)

    if next_url is None:
        return redirect('system:course_videos')
    else:
        return redirect(f'system:{next_url}', course_slug=course_slug)

@csrf_exempt
def payment_canceled(request):
    return render(request, 'system/payment_cancelled.html')



