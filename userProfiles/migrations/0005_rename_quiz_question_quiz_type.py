# Generated by Django 4.2.13 on 2024-05-17 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("userProfiles", "0004_quiz_question_answer"),
    ]

    operations = [
        migrations.RenameField(
            model_name="question",
            old_name="quiz",
            new_name="quiz_type",
        ),
    ]