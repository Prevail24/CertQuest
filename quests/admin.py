from django.contrib import admin
from .models import Quest, Question, UserAnswer

admin.site.register(Quest)
admin.site.register(Question)
admin.site.register(UserAnswer)