# Generated by Django 3.0.3 on 2021-06-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20210615_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
