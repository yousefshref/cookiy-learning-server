# Generated by Django 4.2.5 on 2023-10-19 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_course_review_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_advertise',
            field=models.BooleanField(default=False),
        ),
    ]
