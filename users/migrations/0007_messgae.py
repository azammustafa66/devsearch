# Generated by Django 5.0.6 on 2024-05-15 05:32

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_profile_profile_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Messgae",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("subject", models.CharField(blank=True, max_length=200, null=True)),
                ("body", models.TextField()),
                ("is_read", models.BooleanField(default=False, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "recipient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="messages",
                        to="users.profile",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sender",
                        to="users.profile",
                    ),
                ),
            ],
            options={
                "ordering": ["is_read", "-created_at"],
            },
        ),
    ]
