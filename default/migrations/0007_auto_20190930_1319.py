# Generated by Django 2.2.5 on 2019-09-30 13:19

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0006_meals_cropping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meals',
            name='image',
            field=image_cropping.fields.ImageCropField(upload_to='meals/photo'),
        ),
    ]
