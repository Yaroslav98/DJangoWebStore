# Generated by Django 2.2 on 2019-04-24 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20190423_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rate',
            field=models.FloatField(null=True),
        ),
    ]
