# Generated by Django 2.2.5 on 2019-11-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0030_auto_20191104_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='meals',
            name='location',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
