# Generated by Django 5.0.6 on 2024-05-09 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_tag_project_vote_ratio_project_votes_review_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="value",
            new_name="vote_type",
        ),
    ]