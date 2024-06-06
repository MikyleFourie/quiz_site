# Generated by Django 4.2.13 on 2024-05-20 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiztest', '0005_alter_category_name_alter_question_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='typeOfQ',
            field=models.IntegerField(choices=[(0, 'Multiple Choice'), (1, 'True or False')], default=0, null=True, verbose_name='Type of Question'),
        ),
    ]