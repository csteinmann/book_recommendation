# Generated by Django 4.0.2 on 2023-09-09 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookrec', '0003_alter_choice_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='rotation_state',
            field=models.CharField(default='test', max_length=128, unique=True),
            preserve_default=False,
        ),
    ]