from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'likes': i,
        'content': f'Lorem Ipsum {i}',
    } for i in range(20)
]


def paginate(objects, page, per_page=15):
    paginator = Paginator(QUESTIONS, per_page)
    return paginator.page(page)


# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item})
