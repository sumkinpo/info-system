# Generated by Django 2.1.1 on 2019-04-25 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20190426_0031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='main_image',
        ),
    ]