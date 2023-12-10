import datetime

from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Button, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField
from app.models import Profile, User, Question, Tag, Reply


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


class UserSettingsForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.CharField(label='Email', required=False)
    avatar = forms.ImageField(label='Avatar', required=False)
    password = forms.CharField(min_length=3, widget=forms.PasswordInput, label='New password', required=False)

    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username'),
            Field('email'),
            Field('password'),
            Field('avatar'),
            HTML(
                'Current Avatar<div class="mb-2"><img src="{{stats.user.profile.avatar.url}}" width="128" height="128" alt="User '
                'Avatar"></div>'),
            Submit('submit', 'Submit', css_class='btn btn-success py-2 mt-1')
        )

    def clean_username(self):
        # print(self.request.user.username)
        # print(self.cleaned_data['username'])
        # print(self.cleaned_data['username'] != self.request.user.username)
        if self.cleaned_data['username'] != self.request.user.username and User.objects.filter(
                username=self.cleaned_data['username']).exists():
            raise ValidationError("Username is occupied")
        return self.cleaned_data['username']

    def clean_email(self):
        if self.cleaned_data['email'] != self.request.user.email and User.objects.filter(
                username=self.cleaned_data['email']).exists():
            raise ValidationError("Email is occupied")
        return self.cleaned_data['email']

    def clean_password(self):
        if self.cleaned_data['password'] != '' and len(self.cleaned_data['password']) < 3:
            raise ValidationError("New password is too short (minimum 3 characters)")
        return self.cleaned_data['password']

    def save(self, **kwargs):
        profile = kwargs.pop('profile')
        # print(profile)
        if profile is not None:
            # print(profile.user.username != self.cleaned_data['username'])
            if profile.user.username != self.cleaned_data['username']:
                profile.user.username = self.cleaned_data['username']
            if profile.user.email != self.cleaned_data['email']:
                profile.user.email = self.cleaned_data['email']
            if self.cleaned_data['password'] != '':
                profile.user.set_password(self.cleaned_data['password'])
            if self.cleaned_data['avatar']:
                profile.avatar = self.cleaned_data['avatar']
            profile.user.save()
            profile.save()


# TODO: добавить адеватную валидацию поля username, email, добавить картинки

class AskQuestionForm(forms.Form):
    title = forms.CharField(label='Title', min_length=5,
                            widget=forms.TextInput(
                                attrs={'placeholder': "e.g. How to print 'Hello, World!' in Python?"}))
    text = forms.CharField(label='Text', min_length=10, widget=forms.Textarea(
        attrs={'placeholder': "Type your question here", 'rows': '10'}))
    tags = forms.CharField(label='Tags', required=False, widget=forms.TextInput(
        attrs={'placeholder': "e.g. CSS, c++, golang"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'h5'
        self.helper.layout = Layout(
            Field('title', css_class='input-group mb-3'),
            Field('text', css_class='input-group mb-3'),
            Field('tags', css_class='input-group mb-3'),
            Submit('submit', 'Ask!', css_class='btn btn-success', kwargs={'type': 'submit'})
        )

    def save(self, **kwargs):
        profile = kwargs.pop('profile')
        question = Question(title=self.cleaned_data['title'],
                            content=self.cleaned_data['text'],
                            author=profile,
                            likes=0,
                            creation_time=datetime.datetime.now())
        question.save()
        tagString = self.cleaned_data['tags']
        tags = tagString.casefold().split(',')
        for tagTitle in tags:
            currentTag, _ = Tag.objects.get_or_create(title=tagTitle.strip())
            currentTag.save()
            currentTag.questions.add(question)
            currentTag.save()
        question.save()
        return question


class ReplyForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Type your answer here", 'rows' : '7'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'd-none'
        self.helper.layout = Layout(
            Field('text', css_class='form-control border-dark'),
                Submit('submit', 'Answer!', css_class='btn btn-success rounded-1', kwargs={'type': 'submit'})
        )

    def save(self, **kwargs):
        question = kwargs.pop('question')
        profile = kwargs.pop('profile')
        reply = Reply(question=question, content=self.cleaned_data['text'], author=profile, rating = 0,
                      isCorrect = False, creation_time=datetime.datetime.now())
        reply.save()
        return reply