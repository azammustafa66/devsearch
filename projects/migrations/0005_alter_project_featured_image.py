# Generated by Django 5.0.6 on 2024-05-11 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_project_featured_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="featured_image",
            field=models.ImageField(
                blank=True, default="static/images/default.png", null=True, upload_to=""
            ),
        ),
    ]