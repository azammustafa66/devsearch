# Generated by Django 5.0.6 on 2024-05-15 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_messgae"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Messgae",
            new_name="Message",
        ),
    ]
