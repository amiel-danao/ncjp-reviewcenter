# Generated by Django 4.1.5 on 2023-01-30 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_payment_student'),
        ('job', '0005_alter_certificate_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='review_center',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.reviewcenter'),
        ),
    ]
