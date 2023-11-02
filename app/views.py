from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'likes': i,
        'content': f'Lorem Ipsum {i}',
        'tags': ['CSS', 'Bauman', 'cats'],
    } for i in range(20)
]

QUESTION_REPLY = [
    {
        'content': 'Look at dplyr as a back-end agnostic interface, with all of the targets'
                   'using the same grammer, where you can extend the targets and handlers at will.'
                   'data.table is, from the dplyr perspective, one of those targets.',
        'likes': (3 - i),
    } for i in range(3)
]

STATS = {
    'tags': ['CSS', 'Bamonka', 'offtopic', 'cats', 'memes', 'C++ Programming'],
    'best_members': ['Mr. Freeman', 'Max Payne', 'Carl Johnson', 'Geralt of Rivia', 'John Tanner']
}


def paginate(request, objects, per_page=15):
    page = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, per_page)
    return paginator.page(page)


# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    return render(request, 'index.html',
                  {'questions': paginate(request, QUESTIONS), 'page_title': 'Questions', 'stats': STATS})


def question(request, question_id):
    item = QUESTIONS[question_id]
    replies = QUESTION_REPLY
    return render(request, 'question.html', {'question': item, 'replies': replies, 'stats': STATS})


def ask(request):
    return render(request, 'ask.html', {'stats': STATS})


def hot(request):
    page = request.GET.get('page', 1)
    return render(request, 'index.html',
                  {'questions': paginate(request, QUESTIONS), 'page_title': 'Hot Questions', 'stats': STATS})


def tag(request, tag_id):
    return render(request, 'index.html',
                  {'questions': paginate(request, QUESTIONS), 'page_title': f'Tag: {tag_id}', 'stats': STATS})


def login(request):
    return render(request, 'login.html', {'stats': STATS})


def signup(request):
    return render(request, 'signup.html', {'stats': STATS})
