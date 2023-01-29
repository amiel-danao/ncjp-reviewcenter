from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from authentication.models import CustomUser
from django.core.exceptions import ValidationError
from django import forms
from reviewcenter.managers import CustomUserManager
from authentication.models import Student
from crispy_forms.layout import Field, Div, Layout

PHONE_NUMBER_ATTRS = {'pattern': '[0][0-9]{10}', 'maxlength': '11'}

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

class DateInput(forms.DateInput):
    input_type = 'date'

class StudentProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    contact_person_number = forms.CharField(widget=forms.TextInput(attrs=PHONE_NUMBER_ATTRS), label='Contact No.', required=True)
    # date_of_graduation = forms.DateField(required=True)

    # def __init__(self, *args, **kwargs):
    #     super(StudentProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['school_id'].disabled = True
    #     self.fields['email'].disabled = True
    # def __init__(self, *args, **kwargs):
    #     super(StudentProfileForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Div(
        #         Div(FloatingField('first_name'), css_class='col',),
        #         Div(FloatingField('last_name'), css_class='col',),
        #         css_class='row',
        #     ),
        # )

    class Meta:
        model = Student
        widgets = {
            'date_of_graduation': DateInput(),
        }
        fields = '__all__'
        exclude = ('user', )


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', required=True)

    

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Please confirm your email so you can log in."),
                code='inactive',
            )