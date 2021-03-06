# Generated by Django 2.1.1 on 2019-01-13 18:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ru', models.TextField(blank=True, default='', verbose_name='Наименование')),
                ('name_en', models.TextField(blank=True, default='', verbose_name='Наименование')),
                ('name_other', models.TextField(blank=True, default='', verbose_name='Наименование')),
                ('pseudonym', models.TextField(blank=True, default='', verbose_name='Псевдоним')),
                ('begin_date', models.DateTimeField(blank=True, verbose_name='Дата рождения')),
                ('end_date', models.DateTimeField(blank=True, verbose_name='Дата смерти')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ru', models.TextField(blank=True, default='', verbose_name='Наименование')),
                ('name_en', models.TextField(blank=True, default='', verbose_name='Наименование')),
                ('name_other', models.TextField(blank=True, default='', verbose_name='Наименование')),
                ('begin_date', models.DateTimeField(blank=True, verbose_name='Дата рождения')),
                ('end_date', models.DateTimeField(blank=True, verbose_name='Дата смерти')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('source', models.TextField(blank=True, default='', verbose_name='Источник')),
                ('source_link', models.URLField(blank=True, default='', verbose_name='Ссылка на истчочник')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, upload_to='media', verbose_name='Изображение')),
                ('name_ru', models.TextField(blank=True, default='', verbose_name='Название')),
                ('name_en', models.TextField(blank=True, default='', verbose_name='Название')),
                ('name_other', models.TextField(blank=True, default='', verbose_name='Название')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='core.Author', verbose_name='Автор')),
                ('entity', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='core.Entity', verbose_name='Объект')),
            ],
        ),
        migrations.DeleteModel(
            name='Record',
        ),
    ]
