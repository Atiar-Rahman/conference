from django.db import models
from core.models import BaseModel
from papers.models import Paper
# Create your models here.
class Payment(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payments'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    transaction_id = models.CharField(max_length=255, unique=True)

    gateway = models.CharField(max_length=50, default='stripe')
    currency = models.CharField(max_length=10, default='USD')

    metadata = models.JSONField(null=True, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_id']),
        ]
        ordering = ['-created_at']
