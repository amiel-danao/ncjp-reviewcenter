# Generated by Django 4.1.5 on 2023-01-30 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_certificate_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='file',
            field=models.FileField(blank=True, default='', upload_to='certificate/'),
        ),
    ]
