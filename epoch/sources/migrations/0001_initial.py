# Generated by Django 4.2.6 on 2023-11-04 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('subsribers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Headline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('published', models.DateTimeField()),
                ('img', models.CharField(max_length=255)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sources.source')),
            ],
        ),
    ]
