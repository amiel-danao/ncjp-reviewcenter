# Generated by Django 4.1.5 on 2023-01-29 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_currentreviewcenter'),
        ('system', '0004_alter_payment_options_videocomment_review_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.student'),
        ),
    ]
