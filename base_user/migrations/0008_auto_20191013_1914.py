# Generated by Django 2.2.5 on 2019-10-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_user', '0007_auto_20191005_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user_type',
            field=models.CharField(choices=[('Cooker', 'C'), ('User', 'U')], max_length=30),
        ),
    ]