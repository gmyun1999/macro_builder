# Generated by Django 5.0.6 on 2024-11-14 05:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("macro_sheet", "0006_worksheet_raw_blocks_worksheet_raw_main_block"),
    ]

    operations = [
        migrations.AddField(
            model_name="function",
            name="raw_blocks",
            field=models.JSONField(default=list),
        ),
    ]
