# Generated by Django 4.0.2 on 2023-10-06 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrec', '0003_surveyresponse_sessionid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyresponse',
            old_name='sessionID',
            new_name='sessionId',
        ),
    ]