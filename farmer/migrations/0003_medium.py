# Generated by Django 3.1 on 2020-11-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0002_plant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('soil', models.IntegerField()),
                ('coco', models.IntegerField()),
            ],
        ),
    ]