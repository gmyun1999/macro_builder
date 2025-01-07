# Generated by Django 5.0.6 on 2024-11-06 06:09

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("macro_sheet", "0001_initial"),
        ("user", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gui",
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
                ("name", models.CharField(max_length=255)),
                ("url", models.URLField(max_length=500)),
            ],
            options={
                "db_table": "Gui",
            },
        ),
        migrations.RenameIndex(
            model_name="functionhierarchy",
            new_name="FunctionHie_parent__d40e94_idx",
            old_name="macro_sheet_parent__688daa_idx",
        ),
        migrations.RenameIndex(
            model_name="functionhierarchy",
            new_name="FunctionHie_child_i_455c1c_idx",
            old_name="macro_sheet_child_i_aa62d8_idx",
        ),
        migrations.RenameIndex(
            model_name="worksheetfunction",
            new_name="WorksheetFu_workshe_eaa35d_idx",
            old_name="macro_sheet_workshe_f17537_idx",
        ),
        migrations.RenameIndex(
            model_name="worksheetfunction",
            new_name="WorksheetFu_functio_6fa641_idx",
            old_name="macro_sheet_functio_999d21_idx",
        ),
        migrations.AlterModelTable(
            name="function",
            table="Function",
        ),
        migrations.AlterModelTable(
            name="functionhierarchy",
            table="FunctionHierarchy",
        ),
        migrations.AlterModelTable(
            name="worksheet",
            table="Worksheet",
        ),
        migrations.AlterModelTable(
            name="worksheetfunction",
            table="WorksheetFunction",
        ),
        migrations.AddField(
            model_name="gui",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gui_owner",
                to="user.user",
            ),
        ),
        migrations.AddField(
            model_name="gui",
            name="worksheet",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gui_worksheets",
                to="macro_sheet.worksheet",
            ),
        ),
    ]
