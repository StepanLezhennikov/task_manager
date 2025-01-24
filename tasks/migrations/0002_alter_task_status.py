# Generated by Django 5.1.5 on 2025-01-20 12:50

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("BACKLOG", "Backlog"),
                    ("RUNNING", "Running"),
                    ("DONE", "Done"),
                ],
                default="BACKLOG",
                max_length=10,
            ),
        ),
    ]
