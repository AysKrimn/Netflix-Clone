# Generated by Django 4.2 on 2023-08-28 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_user_app', '0010_alter_netflixprofile_list_delete_netflixprofilelist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='movie_source',
        ),
    ]
