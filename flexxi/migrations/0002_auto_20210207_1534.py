# Generated by Django 2.2.5 on 2021-02-07 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flexxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(upload_to=''),
        ),
    ]