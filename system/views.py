from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.views import View
from django.views.generic.edit import FormMixin, ModelFormMixin, FormView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required as login_required
from django.urls import reverse
from system.forms import VideoCommentForm
from system.models import Course, CoursePrice, Payment, ReviewCenter, Video, VideoComment
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings


def index(request):
    return render(request=request, template_name='index.html')

@login_required
def dashboard(request):
    context = {}
    menu = request.GET.get('menu', None)
    if not menu or menu == 'home':
        pass
    elif menu == 'reviewcenters':
        context['reviewcenters'] = ReviewCenter.objects.filter(active=True)
    elif menu == 'forums':
        context['can_add_question'] = True
    elif menu == 'review':
        context['paid_course_list'] = CoursePrice.objects.filter(price__gt=0, active=True)
        context['free_course_list'] = CoursePrice.objects.filter(price=0, active=True)
    

    return render(request=request, template_name='system/dashboard.html', context=context)

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    
    


class VideoDetailView(LoginRequiredMixin, FormMixin, DetailView):
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
        return reverse('system:video_watch', kwargs={'pk': self.object.id})

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
    context['video_list'] = Video.objects.filter(price=0, active=True)

    return render(request=request, template_name='system/course_videos.html', context=context)

class VideoListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'system/course_videos.html'

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)

        course = get_object_or_404(Course, id=self.kwargs['pk'])
        if course is None:
            raise PermissionDenied()

        context['video_list'] = Video.objects.filter(course=course, active=True)
        context['course'] = course

        return context

# @login_required
# def course_videos(request, id):
#     context = {}
    
#     course = get_object_or_404(Course, id=id)

#     if course is None:
#         raise PermissionDenied()

#     context['video_list'] = Video.objects.filter(course=course, active=True)
#     context['course'] = course

#     return render(request=request, template_name='system/course_videos.html', context=context)

@login_required
def reviewcenter_detail(request, slug):
    instance = ReviewCenter.objects.filter(slug__iexact = slug)
    if instance.exists():
        instance = instance.first()
    else:
        return HttpResponse('<h1>Review Center Not Found</h1>')
    context = {
        'reviewcenter': instance
    }
    return render(request, 'system/reviewcenter_detail.html', context)

@login_required
def check_course_payment(request, pk):
    course = Course.objects.get(id=pk)
    existing_payment = Payment.objects.filter(user=request.user, course=course).first()

    if existing_payment is None:
        return redirect('system:process_payment', pk)
    else:
        return redirect('system:course_videos', pk=pk)

class PaymentView(LoginRequiredMixin, CreateView):
    model = Payment


def process_payment(request, pk):
    course = get_object_or_404(Course, id=pk)
    context = {}
    course_price = CoursePrice.objects.get(course=course)
    context['amount'] = course_price.price
    host = request.get_host()

    price = format(course_price.price, '.2f')

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(price),
        'item_name': course.name,
        'invoice': str(course.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('system:payment_done', kwargs={'pk': pk})),
        'cancel_return': 'http://{}{}'.format(host,
                                              "%s?menu=review" % reverse('system:dashboard')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'system/process_payment.html', {'course': course, 'form': form})

@csrf_exempt
def payment_done(request, pk):
    course = get_object_or_404(Course, id=pk)
    course_price = get_object_or_404(CoursePrice, course=course)
    Payment.objects.create(user=request.user, price=course_price.price, course=course)

    return redirect('system/course_videos.html', pk=pk)


@csrf_exempt
def payment_canceled(request):
    return render(request, 'system/payment_cancelled.html')
