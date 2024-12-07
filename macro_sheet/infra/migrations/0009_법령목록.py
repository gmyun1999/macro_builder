# Generated by Django 5.0.6 on 2024-12-07 15:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("macro_sheet", "0008_rename_gui_id_script_gui"),
    ]

    operations = [
        migrations.CreateModel(
            name="법령목록",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        help_text="ID", primary_key=True, serialize=False
                    ),
                ),
                ("현행연혁코드", models.CharField(help_text="현행연혁코드", max_length=50)),
                ("법령일련번호", models.CharField(help_text="법령일련번호", max_length=50)),
                (
                    "자법타법여부",
                    models.CharField(
                        blank=True, help_text="자법타법여부", max_length=50, null=True
                    ),
                ),
                ("법령상세링크", models.CharField(help_text="법령상세링크", max_length=500)),
                ("법령명한글", models.CharField(help_text="법령명한글", max_length=255)),
                ("법령구분명", models.CharField(help_text="법령구분명", max_length=100)),
                ("소관부처명", models.CharField(help_text="소관부처명", max_length=255)),
                ("공포번호", models.CharField(help_text="공포번호", max_length=50)),
                ("제개정구분명", models.CharField(help_text="제개정구분명", max_length=255)),
                ("소관부처코드", models.CharField(help_text="소관부처코드", max_length=50)),
                ("법령ID", models.CharField(help_text="법령ID", max_length=50)),
                ("공동부령정보", models.TextField(blank=True, help_text="공동부령정보", null=True)),
                ("시행일자", models.CharField(help_text="시행일자", max_length=50)),
                ("공포일자", models.CharField(help_text="공포일자", max_length=50)),
                (
                    "법령약칭명",
                    models.CharField(
                        blank=True, help_text="법령약칭명", max_length=255, null=True
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(auto_now_add=True, help_text="생성일"),
                ),
                ("updated_date", models.DateTimeField(auto_now=True, help_text="수정일")),
            ],
        ),
    ]
