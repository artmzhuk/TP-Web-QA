from django.contrib import admin

# Register your models here.
from .models import Profile, Question, Reply, Tag

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(Tag)
