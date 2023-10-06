# Generated by Django 4.0.2 on 2023-10-06 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookrec', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rotation_state', models.CharField(max_length=128)),
                ('age_group', models.CharField(max_length=128)),
                ('gender', models.CharField(max_length=512)),
                ('reading_platform', models.CharField(max_length=128)),
                ('book_frequency', models.CharField(max_length=128)),
                ('genre', models.CharField(max_length=8192)),
                ('answer', models.ManyToManyField(to='bookrec.Choice')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookrec.survey')),
            ],
        ),
        migrations.DeleteModel(
            name='Submission',
        ),
    ]