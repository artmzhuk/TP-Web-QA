from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count, Sum
from django_resized import ResizedImageField


# Create your models here.


class QuestionManager(models.Manager):
    def replies(self):
        return self.reply_set.all()

    def get_newest(self):
        return self.all().order_by("-creation_time")

    def get_best(self):
        return self.all().order_by("-likes")

    def get_by_tag_best(self, tag_id):
        return self.all().filter(tag__title__iexact=tag_id).order_by("-likes")


class TagManager(models.Manager):
    def get_best_six(self):
        best = self.annotate(q_count=Count('questions')) \
                   .order_by('-q_count')[:6]
        # for i in best:
        #     print(i.q_count, i.title)
        return best


class ProfileManager(models.Manager):
    def create_profile(self, username, email, password, avatar):
        user = User.objects.create_user(username=username, email=email, password=password)
        if avatar is None:
            profile = Profile(user=user)
        else:
            profile = Profile(user=user, avatar=avatar)
        profile.save()
        return

    def get_best_five(self):
        best = self.annotate(q_count=Count('question')) \
                   .order_by('-q_count')[:5]
        # for i in best:
        #     print(i.q_count, i.user.username)
        return best


class ReplyManager(models.Manager):
    def get_best(self):
        return self.all().order_by("-rating")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ResizedImageField(size=[512, 512], crop=['top', 'left'], upload_to='avatars',
                               default='avatars/default.jpg')
    # avatar = models.ImageField(upload_to='avatars')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    likes = models.IntegerField()
    creation_time = models.DateTimeField()

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})

    def get_replies(self):
        return self.reply_set.all()

    def get_best_replies(self):
        return self.reply_set.all().order_by('-rating')

    def tags(self):
        return self.tag_set.all()

    def likes_abs(self):
        return self.likes.__abs__()


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    rating = models.IntegerField()
    isCorrect = models.BooleanField()
    creation_time = models.DateTimeField()

    objects = ReplyManager()

    def __str__(self):
        return self.content


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)
    questions = models.ManyToManyField(Question)

    objects = TagManager()

    def __str__(self):
        return self.title

    def get_num_of_questions(self):
        return self.questions.count()


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    value = models.SmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'author'],
                name='unique_1',
            )
        ]


class ReplyLike(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    value = models.SmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reply', 'author'],
                name='unique_2',
            )
        ]
