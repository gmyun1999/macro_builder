# Generated by Django 5.0.6 on 2024-09-06 07:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.CharField(max_length=36, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(default=None, max_length=64, null=True)),
                ("email", models.CharField(default=None, max_length=64, null=True)),
                ("mobile_no", models.CharField(default=None, max_length=16, null=True)),
                ("oauth_type", models.CharField(max_length=16)),
                ("oauth_id", models.CharField(max_length=64)),
                ("tos_agreed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "User",
                "indexes": [
                    models.Index(fields=["name"], name="User_name_ad0720_idx"),
                    models.Index(fields=["created_at"], name="User_created_2c9361_idx"),
                    models.Index(fields=["updated_at"], name="User_updated_085f8b_idx"),
                ],
                "unique_together": {("oauth_type", "oauth_id")},
            },
        ),
    ]
