# Generated by Django 2.2 on 2020-03-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200302_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=240, unique=True, verbose_name='Post title'),
        ),
    ]
