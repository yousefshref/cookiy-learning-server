# Generated by Django 4.2.5 on 2023-10-18 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_course_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='review',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
