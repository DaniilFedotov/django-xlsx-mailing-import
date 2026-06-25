from django.db import models


class MailingRecord(models.Model):
    """Imported mailing row; external_id prevents duplicate processing."""

    external_id = models.CharField(max_length=255, unique=True, db_index=True)
    user_id = models.PositiveIntegerField()
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mailing Record"
        verbose_name_plural = "Mailing Records"

    def __str__(self) -> str:
        return f"{self.external_id} -> {self.email}"
