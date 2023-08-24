# Generated by Django 4.2 on 2023-08-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_user_app', '0004_alter_netflixprofile_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='netflixprofile',
            name='avatar',
            field=models.FileField(blank=True, default='/static/image/avatar.png', upload_to='Avatars', verbose_name='Fotoğraf'),
        ),
    ]
