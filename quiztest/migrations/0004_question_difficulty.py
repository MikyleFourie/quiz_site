# Generated by Django 4.2.13 on 2024-05-15 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiztest', '0003_remove_question_difficulty_remove_question_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.IntegerField(choices=[(0, 'Beginner'), (1, 'Intermediate'), (2, 'Advanced')], default=0, verbose_name='Difficulty'),
        ),
    ]
