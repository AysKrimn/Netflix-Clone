# Generated by Django 4.2 on 2023-05-15 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0007_netflixprofile_name_alter_netflixprofile_movie_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='netflixuser',
            name='avatar',
        ),
        migrations.AddField(
            model_name='netflixprofile',
            name='avatar',
            field=models.FileField(default='', upload_to='Avatar', verbose_name='User Avatar'),
        ),
        migrations.AddField(
            model_name='netflixprofile',
            name='profile_createdAt',
            field=models.DateTimeField(auto_now=True, verbose_name='Oluşturulma Tarihi'),
        ),
    ]
