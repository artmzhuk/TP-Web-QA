import time

from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Profile, Reply, Tag, QuestionLike, ReplyLike
from django.contrib.auth.models import User
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError

fake = Faker()


class Command(BaseCommand):
    help = 'Fills database with specified ratio'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        if ratio < 15:
            print('ratio must be >= 15')
            return
        start = time.time()

        tags = []
        for i in range(ratio):
            tags.append(Tag(title=f'{fake.word()}{i}'))
        Tag.objects.bulk_create(tags, batch_size=1000)
        tags = Tag.objects.all()
        print(f'Tags created')

        profiles = []
        users = []
        for i in range(ratio - 1):
            print(f'User {i} from {ratio}')
            username = f'{fake.first_name()} {fake.last_name()}{i}'
            user = User(username=username, email=f'{fake.ascii_email()}',
                        password=f'{fake.password(length=10)}')
            users.append(user)
        users.append(User(username='artem@test.by', email=f'artem@test.by', password=make_password(f'123')))
        User.objects.bulk_create(users, batch_size=1000)
        users = User.objects.all()

        for i, user in enumerate(users):
            print(f'Profile {i} from {ratio}')
            username = users[i].username
            with open(f"uploads/avatars/_{username}-ava.png", "wb") as img:
                img.write(fake.image(size=(512, 512)))
            profiles.append(Profile(user=user, avatar=f'avatars/_{username}-ava.png'))
        Profile.objects.bulk_create(profiles, batch_size=1000)
        profiles = Profile.objects.all()

        questions = []
        for i in range(ratio * 10):
            print(f'Question {i} from {ratio * 10}')
            question = Question(title=fake.sentence(nb_words=5),
                                content=fake.paragraph(nb_sentences=5),
                                author=profiles[fake.random_int(min=0, max=len(profiles) - 1)],
                                likes=0,
                                creation_time=fake.date_time_this_century(tzinfo=fake.pytimezone()))
            questions.append(question)
        Question.objects.bulk_create(questions, batch_size=1000)
        questions = Question.objects.all()

        for i, question in enumerate(questions):
            print(f'Tags for question {i} from {ratio * 10}')
            for _ in range(fake.random_int(min=1, max=3)):
                currentTag = tags[fake.random_int(min=0, max=len(tags) - 1)]
                currentTag.questions.add(question)
                currentTag.save()

        questionsLikes = []
        for i, question in enumerate(questions):
            print(f'QuestionLikes for question {i} from {ratio * 10}')
            likeCounter = 0
            baseUserId = fake.random_int(min=0, max=len(profiles) - 1)

            for j in range(15):
                value = fake.boolean() * 2 - 1
                questionLike = QuestionLike(question=question,
                                            author=profiles[(baseUserId + j) % len(profiles)],
                                            value=value)
                questionsLikes.append(questionLike)
                likeCounter += value
            question.likes = likeCounter

        QuestionLike.objects.bulk_create(questionsLikes, batch_size=10000)
        Question.objects.bulk_update(questions, ['likes'], batch_size=1000)
        questions = Question.objects.all()

        replies = []
        for i, question in enumerate(questions):
            print(f'Replies for question {i} from {ratio * 10}')
            for j in range(10):
                reply = Reply(question=question, content=fake.paragraph(nb_sentences=4),
                              author=profiles[fake.random_int(min=0, max=len(profiles) - 1)],
                              rating=0,
                              isCorrect=False,
                              creation_time=fake.date_time_between(start_date=question.creation_time,
                                                                   tzinfo=fake.pytimezone()))
                replies.append(reply)
        Reply.objects.bulk_create(replies, batch_size=10000)
        replies = Reply.objects.all()

        replyLikes = []
        for i, reply in enumerate(replies):
            print(f'Reply likes for question {i} from {ratio * 100}')
            likeCounter = 0
            baseUserId = fake.random_int(min=0, max=len(profiles) - 1)
            for j in range(5):
                value = fake.boolean() * 2 - 1
                replyLike = ReplyLike(reply=reply,
                                      author=profiles[(baseUserId + j) % len(profiles)],
                                      value=value)
                replyLikes.append(replyLike)
                likeCounter += value
            reply.rating = likeCounter

        ReplyLike.objects.bulk_create(replyLikes, batch_size=10000)
        print('Reply likes created')
        Reply.objects.bulk_update(replies, ['rating'], batch_size=2000)

        end = time.time()
        print(f'Time elapsed with ratio={ratio} is {end - start} secs')
