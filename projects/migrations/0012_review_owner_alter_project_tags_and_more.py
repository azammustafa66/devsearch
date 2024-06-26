# Generated by Django 5.0.6 on 2024-05-15 02:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0011_alter_project_options_alter_project_featured_image"),
        ("users", "0005_alter_profile_profile_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="projects.tag"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("owner", "project")},
        ),
    ]
