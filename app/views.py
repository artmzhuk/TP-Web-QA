from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import Question, Tag, Profile
from app.forms import LoginForm, RegisterForm


def paginate(request, objects, per_page=15):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page)
        page_range = paginator.get_elided_page_range(page, on_each_side=1)
    except InvalidPage as e:
        page = 1
        page_obj = paginator.page(page)
        page_range = paginator.get_elided_page_range(page, on_each_side=1)
    return page_obj, page_range


def get_stats(request):
    stats = {
        'tags': Tag.objects.get_best_six(),
        'best_members': Profile.objects.get_best_five(),
        'user': request.user,
    }
    return stats


# Create your views here.
# @login_required(redirect_field_name='continue')
def index(request):
    page_obj, pagination_buttons = paginate(request, Question.objects.get_newest())
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Questions', 'stats': get_stats(request),
                   'pagination': pagination_buttons})


def question(request, question_id):
    item = get_object_or_404(Question, id=question_id)
    page_obj, pagination_buttons = paginate(request, item.get_best_replies())
    return render(request, 'question.html', {'question': item, 'page_obj': page_obj,
                                             'stats': get_stats(request),
                                             'pagination': pagination_buttons})


def ask(request):
    return render(request, 'ask.html', {'stats': get_stats(request)})


def hot(request):  # questions sorted by likes
    page_obj, pagination_buttons = paginate(request, Question.objects.get_best())
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Hot Questions', 'stats': get_stats(request),
                   'pagination': pagination_buttons})


def tag(request, tag_id):
    page_obj, pagination_buttons = paginate(request, Question.objects.get_by_tag_best(tag_id))
    tag_questions_num = get_object_or_404(Tag, title__iexact=tag_id).get_num_of_questions()
    return render(request, 'index.html',
                  {'page_obj': page_obj,
                   'page_title': f'Tag: {tag_id} ({tag_questions_num} questions)',
                   'stats': get_stats(request),
                   'pagination': pagination_buttons})


def login_view(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            print(user)
            if user is not None:
                print('Successful login')
                login(request, user)
                return redirect(request.GET.get('continue', reverse(index)))
            else:
                login_form.add_error(None, 'Wrong password or user does not exist')
    return render(request, 'login.html', {'form': login_form, 'stats': get_stats(request)})


def signup(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect(request.GET.get('continue', reverse(index)))
    return render(request, 'signup.html', {'form': user_form, 'stats': get_stats(request)})


def logout_view(request):
    logout(request)
    return redirect(reverse(index))


def settings(request):
    return render(request, 'settings.html', {'stats': get_stats(request)})
