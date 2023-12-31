# Generated by Django 4.0.2 on 2023-11-13 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookrec', '0005_rotationstate'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponseAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookrec.choice')),
                ('survey_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookrec.surveyresponse')),
            ],
        ),
    ]
