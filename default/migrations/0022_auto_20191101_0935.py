# Generated by Django 2.2.5 on 2019-11-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0021_auto_20191101_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordering',
            name='phone_number',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
