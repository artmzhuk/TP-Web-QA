from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from app.models import Profile


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
    class Meta:
        model = Profile
        fields = '__all__'