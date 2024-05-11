# Generated by Django 5.0.6 on 2024-05-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0009_project_ownser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="featured_image",
            field=models.ImageField(
                blank=True,
                default="images/projects/project-default.png",
                null=True,
                upload_to="images/projects/",
            ),
        ),
    ]