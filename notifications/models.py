from django.db import models
from core.models import BaseModel

# Create your models here.
class Notification(BaseModel):
    NOTIFICATION_TYPES = (
        ('review', 'Review'),
        ('paper', 'Paper'),
        ('system', 'System'),
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']