# Generated by Django 4.2.6 on 2023-12-15 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='complete',
            field=models.BooleanField(default=False, verbose_name='完了チェック'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=200, null=True, verbose_name='タイトル'),
        ),
    ]
