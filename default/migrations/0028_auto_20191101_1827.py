# Generated by Django 2.2.5 on 2019-11-01 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0027_auto_20191101_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordering',
            name='delivery_type',
            field=models.CharField(blank=True, choices=[('User', 'User'), ('Shef', 'Shef')], default='User', max_length=244, null=True),
        ),
    ]