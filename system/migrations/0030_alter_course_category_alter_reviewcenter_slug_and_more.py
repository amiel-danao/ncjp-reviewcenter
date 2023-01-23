# Generated by Django 4.1.5 on 2023-01-23 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0029_alter_course_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.SlugField(allow_unicode=True, default='', max_length=255, unique=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='reviewcenter',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', max_length=255, unique=True),
        ),
    ]