# Generated by Django 2.2 on 2019-05-10 16:33

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20190510_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(default='/media/default_user_icon.jpg', upload_to=store.models.user_directory_path),
        ),
    ]
