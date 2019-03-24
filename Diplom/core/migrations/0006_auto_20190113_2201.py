# Generated by Django 2.1.1 on 2019-01-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190113_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='begin_date',
            field=models.DateField(verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='end_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата окончания'),
        ),
    ]