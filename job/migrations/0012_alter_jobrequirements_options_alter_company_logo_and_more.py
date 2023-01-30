# Generated by Django 4.1.5 on 2023-01-30 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0011_companyindustry_review_center'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobrequirements',
            options={'verbose_name_plural': 'Job Requirements'},
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='', upload_to='company_logos/'),
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(default='', upload_to='resumes/')),
                ('expected_salary', models.PositiveBigIntegerField(default=0)),
                ('message_to_employer', models.CharField(blank=True, default='', max_length=255)),
                ('job_post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='job.jobpost')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
