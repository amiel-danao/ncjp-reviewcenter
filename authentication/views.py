from django.views.generic import CreateView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as authlogout
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from smtplib import SMTPDataError
from django.contrib.auth.decorators import login_required as login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from authentication.forms import LoginForm, RegisterForm, StudentProfileForm
from authentication.models import CurrentReviewCenter, CustomUser, StudentProgress
from system.context_processors import EMAIL_VERIFY_SENDER, EMAIL_VERIFY_SUBJECT
from authentication .models import Student
from system.models import Course
from system.views import StudentOnlyMixin


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.is_active = False
            user.save()
            Student.objects.create(user=user,
                                    first_name=request.POST.get('first_name', ''),
                                    middle_name=request.POST.get('middle_name', ''),
                                    last_name=request.POST.get('last_name', ''))
            
            # login(request, user)
            try:
                domain = request.get_host()
                link = reverse('authentication:create', kwargs={'id':user.id})
                send_verification_email(request.POST.get('email'), f'{domain}{link}')
                messages.success(request, "Registration successful. Please check your email to verify your account.")
                return redirect('system:index')
            except SMTPDataError as error:
                messages.error(request, f'{error}\n Please try again later.', extra_tags="form_error")
                return redirect('system:index')
        else:
            messages.error(request, form.errors, extra_tags="form_error")
            for key, error in form.error_messages.items():
                messages.error(request, error, extra_tags="form_error")
        
    return render(request=request, template_name="index.html", context={"form": form})

@login_required
def logout_view(request):
    authlogout(request)

    return redirect('system:index')

def send_verification_email(email, link):
    send_mail(
        EMAIL_VERIFY_SUBJECT,
        f'To verify your account, please follow this link: {link} \n Please disregard this email if you do not create this account!',
        EMAIL_VERIFY_SENDER,
        (email, ),
        fail_silently=False,
    )

def verify_account_view(request, id):
    if request.method == "GET":
        account = CustomUser.objects.get(id=id)
        if not account.is_active:
            account.is_active = True
            account.save()
            messages.success(request, f'Your account is now verified, Proceed to login')
        return render(request=request, template_name='index.html')
    return HttpResponseBadRequest()


def verification(request):
    return render(request=request, template_name="authentication/verification.html")

def send_verification(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        if email is not None:
            try:
                user = CustomUser.objects.get(email=email)
                if user.is_active:
                    messages.error(request, f'User with email {email} is already registered')
                    return redirect('authentication:login')
            except CustomUser.DoesNotExist:
                messages.error(request, f'User with email {email} is not yet registered')
                return redirect('system:index')
            try:
                domain = request.get_host()
                link = reverse('authentication:create', kwargs={'id':user.id})
                send_verification_email(email, f'{domain}{link}')
                messages.success(request, f'An email verification was sent to {email}.')
                return redirect('system:index')
            except SMTPDataError as error:
                messages.error(request, f'{error}\n Please try again later.')
                return redirect('system:index')

    return HttpResponseBadRequest()

class CustomLoginView(auth_views.LoginView): # 1. <--- note: this is a class-based view
    
    form_class = LoginForm # 2. <--- note: define form here?

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('system:index')

    def get_context_data(self, **kwargs):
        #context = super(LoginView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        for key, error in form.error_messages.items():
            messages.error(self.request, error, extra_tags="form_error")
        return self.render_to_response(context)


class StudentProfileCreateView(StudentOnlyMixin, LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentProfileForm
    template_name = 'system/review_center_regform.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user if user else None
        return super(StudentProfileCreateView, self).form_valid(form)

    # def get_success_url(self):
    #     return reverse('lawyer_detail', kwargs={'lawyer_slug': self.object.lawyer_slug})

    def get_context_data(self, **kwargs):
        context = super(StudentProfileCreateView, self).get_context_data(**kwargs)
        
        context['active_link'] = 'reg_form'
            
        return context

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


    
class StudentProfileUpdateView(StudentOnlyMixin, LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentProfileForm
    template_name = 'system/review_center_regform.html'

    def get_context_data(self, **kwargs):
        context = super(StudentProfileUpdateView, self).get_context_data(**kwargs)
        
        context['form'] = StudentProfileForm(initial=self.object.__dict__)
        context['active_link'] = 'reg_form'
            
        return context

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_success_url(self):

        current, _ = CurrentReviewCenter.objects.get_or_create(user=self.request.user)

        course_slug = self.request.GET.get('course', None)
        if current is None or current.review_center is None or course_slug is None:
            return reverse('system:dashboard')
        
        course = Course.objects.filter(category=course_slug).first()
        if course is None:
            return reverse('system:dashboard')

        progress, created = StudentProgress.objects.get_or_create(user=self.request.user, review_center=current.review_center)
        progress.course = course
        progress.save()


        return reverse("system:check_course_payment", kwargs={'course_slug': course_slug})


class StudentProfileRedirectView(RedirectView):

   def get_redirect_url(self, *args, **kwargs):

        student = Student.objects.filter(user=self.request.user).first()

        course_slug = kwargs.get('course_slug',"")

        if student is not None:
            url = f"%s?course={course_slug}" % reverse("authentication:update_reg_form", kwargs={'pk': student.pk})
            return url#reverse("authentication:update_reg_form", kwargs={'pk': student.pk, 'course_slug': course_slug})
    
        return reverse("authentication:registration_form", kwargs={'course_slug': course_slug})