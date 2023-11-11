import random
import string
import time

from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Profile, Reply, Tag
from django.contrib.auth.models import User
from faker import Faker
from django.db.utils import IntegrityError

fake = Faker()


class Command(BaseCommand):
    help = 'Fills database with specified ratio'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        start = time.time()

        tags = []
        for i in range(ratio):
            try:
                tags.append(Tag.objects.create(title=fake.word()))
            except IntegrityError:
                tags.append(Tag.objects.create(title=f'{fake.word()}{i}'))
        print(f'Tags created')

        profiles = []
        for i in range(ratio):
            print(f'User {i}')
            username = f'{fake.first_name()} {fake.last_name()}'
            try:
                user = User.objects.create_user(username, f'{fake.ascii_email()}', f'{fake.password(length=10)}')
            except IntegrityError:
                username = f'{fake.first_name()} {fake.last_name()}i'
                user = User.objects.create_user(username, f'{fake.ascii_email()}', f'{fake.password(length=10)}')
            with open(f"uploads/avatars/_{username}-ava.png", "wb") as img:
                img.write(fake.image(size=(512, 512)))
            profiles.append(Profile.objects.create(user=user, avatar=f'avatars/_{username}-ava.png'))

        for j in range(ratio * 10):
            print(f'Question {j} from {ratio * 10}')
            question = Question.objects.create(title=fake.sentence(nb_words=5),
                                               content=fake.paragraph(nb_sentences=5),
                                               author=profiles[fake.random_int(min=0, max=len(profiles) - 1)],
                                               likes=fake.random_int(min=-ratio, max=ratio),
                                               creation_time=fake.date_time_this_century(tzinfo=fake.pytimezone()))
            for _ in range(fake.random_int(min=1, max=4)):
                tags[fake.random_int(min=0, max=len(tags) - 1)].questions.add(question)
            for k in range(10):
                reply = Reply.objects.create(question=question, content=fake.paragraph(nb_sentences=4),
                                             author=profiles[fake.random_int(min=0, max=len(profiles) - 1)],
                                             rating=fake.random_int(min=-100, max=100),
                                             isCorrect=False,
                                             creation_time=fake.date_time_between(start_date=question.creation_time,
                                                                                  tzinfo=fake.pytimezone()))
        end = time.time()
        print(f'Time elapsed with ratio={ratio} is {end - start} secs')
