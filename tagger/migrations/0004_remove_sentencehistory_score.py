# Generated by Django 2.1.7 on 2019-02-27 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tagger', '0003_auto_20190227_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentencehistory',
            name='score',
        ),
    ]
