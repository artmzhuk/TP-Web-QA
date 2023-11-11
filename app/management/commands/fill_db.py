import random

from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Profile, Reply, Tag
from django.contrib.auth.models import User

CONTENT = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et "
           "dolore"
           " magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
           "commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat "
           "nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit "
           "anim id est laborum.")


class Command(BaseCommand):
    help = 'Fills database with specified ratio'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        tags = []
        for i in range(ratio):
            tags.append(Tag.objects.create(title=f'tag{i}'))
        for i in range(ratio):
            user = User.objects.create_user(f"user{i}", f"user{i}.test.com", f"user{i}password")
            profile = Profile.objects.create(user=user, avatar='uploads/avatars/eminem-ava.png')
            for j in range(10):
                question = Question.objects.create(title=f'Question{i * 10 + j}', content=f'{i * 10 + j}{CONTENT}',
                                                   author=profile,
                                                   likes=j)
                for _ in range(3):
                    tags[random.randint(0, len(tags) - 1)].questions.add(question)
                for k in range(10):
                    reply = Reply.objects.create(question=question, content=f'reply {k} for {i * 10 + j}{CONTENT}',
                                                 author=profile, rating=k, isCorrect=False)
