# Generated by Django 2.2.5 on 2019-11-01 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0026_auto_20191101_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meals',
            name='delivery_type',
            field=models.CharField(choices=[('User', 'User'), ('Shef', 'Shef')], default='User', max_length=244),
        ),
    ]