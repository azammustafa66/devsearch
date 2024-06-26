# Generated by Django 5.0.6 on 2024-05-14 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0010_alter_project_featured_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterField(
            model_name="project",
            name="featured_image",
            field=models.ImageField(
                blank=True,
                default="/projects/project-default.png",
                null=True,
                upload_to="images/projects/",
            ),
        ),
    ]
