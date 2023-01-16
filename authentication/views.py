from django.contrib.auth import logout as authlogout
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from smtplib import SMTPDataError
from django.contrib.auth.decorators import login_required as login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from authentication.forms import LoginForm, RegisterForm
from authentication.models import CustomUser
from system.context_processors import EMAIL_VERIFY_SUBJECT
from system.models import Student


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            Student.objects.create(email=user.email, 
                                    first_name=request.POST.get('first_name', ''),
                                    middle_name=request.POST.get('middle_name', ''),
                                    last_name=request.POST.get('last_name', ''))
            # login(request, user)
            try:
                domain = request.get_host()
                link = reverse('system:create', kwargs={'id':user.id})
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
        'ncst.kiosk.gmail.com',
        (email, ),
        fail_silently=False,
    )

def verify_account_view(request, id):
    if request.method == "GET":
        account = CustomUser.objects.get(id=id)
        account.is_active = True
        account.save()
        return render(request=request, template_name='registration/verified.html')
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
                return redirect('authentication:register')
            try:
                domain = request.get_host()
                link = reverse('authentication:create', kwargs={'id':user.id})
                send_verification_email(request.POST.get('email'), f'{domain}{link}')
                messages.success(request, f'An email verification was sent to {email}.')
                return redirect('authentication:register')
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