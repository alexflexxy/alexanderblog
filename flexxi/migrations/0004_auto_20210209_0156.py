# Generated by Django 2.2.5 on 2021-02-09 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexxi', '0003_auto_20210209_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
