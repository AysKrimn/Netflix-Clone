# Generated by Django 4.2 on 2023-05-19 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0009_alter_netflixprofile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='netflixprofile',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True, verbose_name='Profil İlk Adı'),
        ),
    ]
