# Generated by Django 2.2.5 on 2019-10-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0009_auto_20191014_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_photo',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='', verbose_name='profilephoto'),
        ),
    ]