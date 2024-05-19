# Generated by Django 4.2.13 on 2024-05-19 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiztest', '0003_alter_answer_question_alter_question_quiz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='is_right',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')], default=0, null=True, verbose_name='Difficulty'),
        ),
    ]