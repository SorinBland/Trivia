# Generated by Django 3.0.3 on 2021-06-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20210605_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answers',
            name='question',
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ManyToManyField(to='quiz.Questions'),
        ),
    ]
