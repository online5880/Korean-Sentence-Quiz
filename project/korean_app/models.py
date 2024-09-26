from django.db import models
from django.utils import timezone

class Sentence(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class QuizResult(models.Model):
    nickname = models.CharField(max_length=50, default='Anonymous')  # 이 줄을 추가합니다
    score = models.IntegerField()
    time_taken = models.DurationField()
    completed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Score: {self.score}, Time: {self.time_taken}"
    
class QuizLog(models.Model):
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name='logs')
    sentence = models.TextField()  # 전체 문장
    target_word = models.CharField(max_length=100)  # 질문 대상 단어
    correct_answer = models.CharField(max_length=100)
    user_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField()
    time_taken = models.DurationField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sentence: {self.sentence[:30]}, Word: {self.target_word}, Correct: {self.is_correct}"