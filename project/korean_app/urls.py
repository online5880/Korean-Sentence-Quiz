from django.urls import path
from . import views

urlpatterns = [
    path('text-analysis/', views.set_nickname, name='set_nickname'),
    path('text-analysis/quiz/', views.quiz, name='quiz'),
    path('text-analysis/check_answer/', views.check_answer, name='check_answer'),
    path('text-analysis/save_quiz_result/', views.save_quiz_result, name='save_quiz_result'),
    path('text-analysis/get_random_sentence/', views.get_random_sentence, name='get_random_sentence'),
    path('text-analysis/results/', views.show_results, name='show_results'),
]