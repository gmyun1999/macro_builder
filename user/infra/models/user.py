from django.db import models


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=64, default=None, null=True)
    email = models.CharField(max_length=64, default=None, null=True)
    mobile_no = models.CharField(max_length=16, default=None, null=True)
    oauth_type = models.CharField(max_length=16)
    oauth_id = models.CharField(max_length=64)
    tos_agreed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "User"
        unique_together = ("oauth_type", "oauth_id")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]
