# Generated by Django 2.2.5 on 2019-10-30 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0013_auto_20191028_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='facebook',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='instagram',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='twitter',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
    ]
