from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render
from app.models import Question, Tag, Profile


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


def get_stats():
    stats = {
        'tags': Tag.objects.get_best_six(),
        'best_members': Profile.objects.get_best_five()
    }
    return stats


# Create your views here.
def index(request):
    page_obj, pagination_buttons = paginate(request, Question.objects.get_newest())
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Questions', 'stats': get_stats(),
                   'pagination': pagination_buttons})


def question(request, question_id):
    item = Question.objects.get(id=question_id)
    page_obj, pagination_buttons = paginate(request, item.get_best_replies())
    return render(request, 'question.html', {'question': item, 'page_obj': page_obj,
                                             'stats': get_stats(),
                                             'pagination': pagination_buttons})


def ask(request):
    return render(request, 'ask.html', {'stats': get_stats()})


def hot(request):  # questions sorted by likes
    page_obj, pagination_buttons = paginate(request, Question.objects.get_best())
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Hot Questions', 'stats': get_stats(),
                   'pagination': pagination_buttons})


def tag(request, tag_id):
    page_obj, pagination_buttons = paginate(request, Question.objects.get_by_tag_best(tag_id))
    tag_questions_num = Tag.objects.get(title__iexact=tag_id).get_num_of_questions()
    return render(request, 'index.html',
                  {'page_obj': page_obj,
                   'page_title': f'Tag: {tag_id} ({tag_questions_num} questions)',
                   'stats': get_stats(),
                   'pagination': pagination_buttons})


def login(request):
    return render(request, 'login.html', {'stats': get_stats()})


def signup(request):
    return render(request, 'signup.html', {'stats': get_stats()})


def settings(request):
    return render(request, 'settings.html', {'stats': get_stats()})
