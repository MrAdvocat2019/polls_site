# Generated by Django 5.0.1 on 2024-02-03 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_answer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'permissions': (('can_nullify', 'User can nullify votes'),)},
        ),
    ]