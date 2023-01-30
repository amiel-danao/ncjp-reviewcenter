# Generated by Django 4.1.5 on 2023-01-30 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0004_alter_quiz_exam_paper_alter_quiz_random_order'),
        ('job', '0017_jobapplication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.companyindustry'),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='company',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.company'),
        ),
        migrations.AlterField(
            model_name='jobrequirements',
            name='certificate_quiz',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz'),
        ),
    ]
