from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('ask', views.ask, name='ask'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/<tag_id>', views.tag, name='tag'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('settings', views.settings, name='settings'),
]
