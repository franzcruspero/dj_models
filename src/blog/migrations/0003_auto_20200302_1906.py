# Generated by Django 2.2 on 2020-03-02 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200302_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.CharField(choices=[('draft', 'Draft'), ('publish', 'Publish'), ('private', 'Private')], default='draft', max_length=120),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=240, verbose_name='Post title'),
        ),
    ]