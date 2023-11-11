from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class ReplyManager(models.Manager):
    pass


class QuestionManager(models.Manager):
    def replies(self):
        return self.reply_set.all()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/avatars')


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    likes = models.IntegerField()
    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})

    def replies(self):
        return self.reply_set.all()

    def tags(self):
        return self.tag_set.all()


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    rating = models.IntegerField()
    isCorrect = models.BooleanField()

    def __str__(self):
        return self.content


class Tag(models.Model):
    title = models.CharField(max_length=30)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title
