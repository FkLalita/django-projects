from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Profile, Question, Answer, Comment

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
