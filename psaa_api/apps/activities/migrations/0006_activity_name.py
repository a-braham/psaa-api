# Generated by Django 3.2.12 on 2022-09-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_alter_activity_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]