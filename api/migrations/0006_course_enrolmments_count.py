# Generated by Django 4.2.5 on 2023-10-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_userprofile_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='enrolmments_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
