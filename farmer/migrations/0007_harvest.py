# Generated by Django 3.1 on 2020-11-26 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0006_auto_20201126_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Harvest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('output', models.IntegerField()),
                ('tray', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farmer.tray')),
            ],
        ),
    ]