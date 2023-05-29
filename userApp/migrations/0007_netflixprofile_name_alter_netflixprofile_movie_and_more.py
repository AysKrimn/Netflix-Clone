# Generated by Django 4.2 on 2023-05-15 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0006_netflixprofile_netflixuser_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='netflixprofile',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='Profil Adı'),
        ),
        migrations.AlterField(
            model_name='netflixprofile',
            name='movie',
            field=models.ManyToManyField(default=1, to='userApp.movies', verbose_name='Favori Listesi'),
        ),
        migrations.AlterField(
            model_name='netflixprofile',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ana Hesabı'),
        ),
    ]
