# Generated by Django 4.2.16 on 2024-09-25 13:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('korean_app', '0002_quizresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('correct_answer', models.CharField(max_length=100)),
                ('user_answer', models.CharField(max_length=100)),
                ('is_correct', models.BooleanField()),
                ('time_taken', models.DurationField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='korean_app.quizresult')),
            ],
        ),
    ]
