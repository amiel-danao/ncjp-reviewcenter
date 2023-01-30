# Generated by Django 4.1.5 on 2023-01-30 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_quiz_single_attempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='exam_paper',
            field=models.BooleanField(default=True, help_text='If yes, the result of each attempt by a user will be stored. Necessary for marking.', verbose_name='Exam Paper'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='random_order',
            field=models.BooleanField(default=True, help_text='Display the questions in a random order or as they are set?', verbose_name='Random Order'),
        ),
    ]