# Generated by Django 3.1 on 2020-11-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0004_tray'),
    ]

    operations = [
        migrations.AddField(
            model_name='tray',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
