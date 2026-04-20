from django.db import models
from core.models import BaseModel
from conferences.models import Track
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Paper(BaseModel):
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        UNDER_REVIEW = 'under_review', 'Under Review'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='papers')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='papers')

    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.CharField(max_length=255)

    pdf = models.FileField(upload_to='paper/')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED
    )
    


class CoAuthor(BaseModel):
    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name="co_authors"
    )

    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coauthored_papers"
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    institution = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["paper", "user"],
                name="unique_user_per_paper"
            )
        ]

class ReviewAssignment(BaseModel):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="assignments")
    reviewer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="review_assignments")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['paper', 'reviewer'],
                name='unique_reviewer_per_paper'
            )
        ]

class Review(BaseModel):
    class Recommendation(models.TextChoices):
        ACCEPT = 'accept', 'Accept'
        REJECT = 'reject', 'Reject'
        REVISION = 'revision', 'Revision'

    assignment = models.OneToOneField(
        ReviewAssignment,
        on_delete=models.CASCADE,
        related_name="review"
    )

    comment = models.TextField()
    plagiarism_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    ai_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    recommendation = models.CharField(
        max_length=20,
        choices=Recommendation.choices
        )
    