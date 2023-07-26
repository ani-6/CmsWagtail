# Generated by Django 4.2.3 on 2023-07-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_url', models.URLField(blank=True, verbose_name='Twitter URL')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub URL')),
                ('organisation_url', models.URLField(blank=True, verbose_name='Organisation URL')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
