# Generated by Django 5.1.4 on 2024-12-26 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Project Name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Project Description"),
                ),
                ("logo_url", models.URLField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProjectUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.BigIntegerField()),
                ("user_email", models.EmailField(max_length=255)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("reader", "Reader"),
                            ("editor", "Editor"),
                            ("owner", "Owner"),
                        ],
                        default="reader",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_users",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "user_id")},
            },
        ),
    ]
