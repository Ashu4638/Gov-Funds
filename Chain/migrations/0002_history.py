# Generated by Django 3.2.9 on 2022-01-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('ID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('fromAdd', models.TextField()),
                ('toAdd', models.TextField()),
                ('amount', models.IntegerField()),
                ('timestamp', models.TextField()),
                ('status', models.TextField()),
            ],
        ),
    ]
