from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
from app.models import Profile, User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField('username', css_class='form-control'),
            FloatingField('password', css_class='form-control'),
            Submit('submit', 'Submit', css_class='btn btn-primary w-100 py-2')
        )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=3, widget=forms.PasswordInput)

    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise ValidationError("Username is occupied")

        if User.objects.filter(username=self.cleaned_data['email']).exists():
            raise ValidationError("Email is occupied")
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise ValidationError("Passwords do not match")

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        Profile.objects.create_profile(**self.cleaned_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('email'),
            Field('password'),
            Field('password_check'),
            Field('avatar'),
            Submit('submit', 'Submit', css_class='btn btn-success py-2 mt-1')
        )
