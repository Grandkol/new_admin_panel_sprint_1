# Generated by Django 4.2.11 on 2024-07-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='type',
            field=models.CharField(choices=[('movie', 'movie'), ('tv_show', 'tv_show')], default='movie'),
        ),
    ]
