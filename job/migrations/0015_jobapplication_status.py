# Generated by Django 4.1.5 on 2023-01-30 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0014_alter_jobapplication_job_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'For interview'), (3, 'For Requirements'), (4, 'HIRED')], default=1),
        ),
    ]
