# Generated by Django 3.2.12 on 2022-09-07 02:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0009_2_auto_20220907_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='isibo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='student_isibo', to='schools.isibo'),
            preserve_default=False,
        ),
    ]