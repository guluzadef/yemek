# Generated by Django 2.2.5 on 2019-09-30 13:12

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0005_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='meals',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '500x500', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
