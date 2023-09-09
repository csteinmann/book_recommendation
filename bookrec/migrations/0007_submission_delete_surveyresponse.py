# Generated by Django 4.0.2 on 2023-09-09 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookrec', '0006_surveyresponse_delete_submission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200)),
                ('answer', models.ManyToManyField(to='bookrec.Choice')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookrec.survey')),
            ],
        ),
        migrations.DeleteModel(
            name='SurveyResponse',
        ),
    ]
