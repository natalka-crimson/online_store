# Generated by Django 5.0.4 on 2024-09-09 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=0, upload_to='category_images/'),
            preserve_default=False,
        ),
    ]
