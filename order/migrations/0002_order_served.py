# Generated by Django 3.1.1 on 2020-09-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='served',
            field=models.BooleanField(default=False),
        ),
    ]
