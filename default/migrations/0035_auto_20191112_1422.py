# Generated by Django 2.2.7 on 2019-11-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0034_menu_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='menuicon'),
        ),
    ]
