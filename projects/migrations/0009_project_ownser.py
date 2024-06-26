# Generated by Django 5.0.6 on 2024-05-11 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0008_alter_project_featured_image"),
        ("users", "0002_profile_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="ownser",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.profile",
            ),
        ),
    ]
