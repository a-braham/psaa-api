# Generated by Django 3.2.12 on 2022-09-07 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20220907_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='parent_name',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='parent_tel',
        ),
    ]
