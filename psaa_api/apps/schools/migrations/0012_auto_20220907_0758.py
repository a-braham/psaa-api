# Generated by Django 3.2.12 on 2022-09-07 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0011_auto_20220907_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='district',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='province',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
