# Generated by Django 4.1 on 2024-04-03 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_photo_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(to='blog.photo', verbose_name='Зображення'),
        ),
    ]