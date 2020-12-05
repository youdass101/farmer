# Generated by Django 3.1 on 2020-12-05 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0012_auto_20201206_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerOld',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TextField(blank=True, null=True)),
                ('medium_weight', models.IntegerField(blank=True, null=True)),
                ('seeds_weight', models.IntegerField(blank=True, null=True)),
                ('medium_id', models.IntegerField(blank=True, null=True)),
                ('name_id', models.IntegerField(blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('fname', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
