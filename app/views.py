from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'likes': i,
        'content': f'Lorem Ipsum {i}',
        'tags': ['CSS', 'Bauman', 'cats'],
    } for i in range(2500)
]

QUESTION_REPLY = [
    {
        'content': 'Look at dplyr as a back-end agnostic interface, with all of the targets'
                   'using the same grammer, where you can extend the targets and handlers at will.'
                   'data.table is, from the dplyr perspective, one of those targets.',
        'likes': (50 - i),
    } for i in range(50)
]

STATS = {
    'tags': ['CSS', 'Bamonka', 'offtopic', 'cats', 'memes', 'C++ Programming'],
    'best_members': ['Mr. Freeman', 'Max Payne', 'Carl Johnson', 'Geralt of Rivia', 'John Tanner']
}


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


# Create your views here.
def index(request):
    page_obj, pagination_buttons = paginate(request, QUESTIONS)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Questions', 'stats': STATS,
                   'pagination': pagination_buttons})


def question(request, question_id):
    item = QUESTIONS[question_id]
    page_obj, pagination_buttons = paginate(request, QUESTION_REPLY)
    return render(request, 'question.html', {'question': item, 'page_obj': page_obj, 'stats': STATS,
                                             'pagination': pagination_buttons})


def ask(request):
    return render(request, 'ask.html', {'stats': STATS})


def hot(request):
    page_obj, pagination_buttons = paginate(request, QUESTIONS)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Hot Questions', 'stats': STATS,
                   'pagination': pagination_buttons})


def tag(request, tag_id):
    page_obj, pagination_buttons = paginate(request, QUESTIONS)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': f'Tag: {tag_id}', 'stats': STATS,
                   'pagination': pagination_buttons})


def login(request):
    return render(request, 'login.html', {'stats': STATS})


def signup(request):
    return render(request, 'signup.html', {'stats': STATS})


def settings(request):
    return render(request, 'settings.html', {'stats': STATS})
