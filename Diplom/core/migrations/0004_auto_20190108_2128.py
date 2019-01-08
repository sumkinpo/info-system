# Generated by Django 2.1.1 on 2019-01-08 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20181216_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='author',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Author', to='core.Author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='image',
            name='object',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Entity', to='core.Entity', verbose_name='Объект'),
        ),
    ]
