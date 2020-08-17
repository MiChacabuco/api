# Generated by Django 2.2.12 on 2020-08-17 22:29

from django.db import migrations, models
import michacabuco_admin.businesses.validators


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Logo o imagen de su comercio/negocio. Tamaño máximo: 5MB.', null=True, upload_to='avatars', validators=[michacabuco_admin.businesses.validators.validate_image_size], verbose_name='avatar'),
        ),
    ]
