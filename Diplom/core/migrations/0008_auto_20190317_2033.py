# Generated by Django 2.1.1 on 2019-03-17 17:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190116_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Псевдоним')),
            ],
        ),
        migrations.CreateModel(
            name='AuthorsSpecialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.TextField(verbose_name='Специальность')),
            ],
        ),
        migrations.RemoveField(
            model_name='author',
            name='pseudonym',
        ),
        migrations.RemoveField(
            model_name='image',
            name='author',
        ),
        migrations.AddField(
            model_name='author',
            name='index',
            field=models.TextField(blank=True, default='', verbose_name='Индекс'),
        ),
        migrations.AddField(
            model_name='author',
            name='notes',
            field=models.TextField(blank=True, default='', verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='entity',
            name='index',
            field=models.TextField(blank=True, default='', verbose_name='Индекс'),
        ),
        migrations.AddField(
            model_name='entity',
            name='notes',
            field=models.TextField(blank=True, default='', verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='image',
            name='create_data',
            field=models.TextField(blank=True, default='', verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='image',
            name='description_lat',
            field=models.TextField(blank=True, default='', verbose_name='Описание lat'),
        ),
        migrations.AddField(
            model_name='image',
            name='notes',
            field=models.TextField(blank=True, default='', verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='image',
            name='source_link',
            field=models.URLField(blank=True, default='', verbose_name='Ссылка на источник'),
        ),
        migrations.AlterField(
            model_name='author',
            name='begin_date',
            field=models.TextField(blank=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='author',
            name='end_date',
            field=models.TextField(blank=True, verbose_name='Дата смерти'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='begin_date',
            field=models.TextField(verbose_name='Дата начала'),
        ),
        migrations.RemoveField(
            model_name='entity',
            name='category',
        ),
        migrations.AddField(
            model_name='entity',
            name='category',
            field=models.ManyToManyField(to='core.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='end_date',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='source_link',
            field=models.URLField(blank=True, default='', verbose_name='Ссылка на источник'),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания в базе'),
        ),
        migrations.AlterField(
            model_name='image',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения в базе'),
        ),
        migrations.AddField(
            model_name='authorsspecialization',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.Author', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='authorsspecialization',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='core.Image', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='authoralias',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Author', verbose_name='Автор'),
        ),
    ]
