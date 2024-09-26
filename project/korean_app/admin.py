from django.contrib import admin

# Register your models here.
from .models import Sentence, QuizResult, QuizLog

admin.site.register(Sentence)
admin.site.register(QuizResult)
admin.site.register(QuizLog)