from django.utils.translation import gettext as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from authentication.models import CustomUser
from django.core.exceptions import ValidationError
from django import forms
from reviewcenter.managers import CustomUserManager
from system.models import Student



class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class StudentProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['school_id'].disabled = True
        self.fields['email'].disabled = True

    class Meta:
        model = Student
        fields = '__all__'


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', required=True)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Please confirm your email so you can log in."),
                code='inactive',
            )