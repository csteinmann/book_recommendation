# Generated by Django 4.0.2 on 2023-10-06 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookrec', '0002_surveyresponse_delete_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='sessionID',
            field=models.CharField(default='x', max_length=128),
            preserve_default=False,
        ),
    ]
