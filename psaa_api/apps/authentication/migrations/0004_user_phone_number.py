# Generated by Django 3.2.12 on 2022-07-05 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='', max_length=100),
        ),
    ]
