# Generated by Django 3.2.3 on 2021-06-01 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkList', '0003_checklistitems_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistdata',
            name='userName',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
    ]