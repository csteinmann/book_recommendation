# Generated by Django 4.0.2 on 2023-09-27 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookrec', '0005_alter_submission_rotation_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='rotation_state',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
