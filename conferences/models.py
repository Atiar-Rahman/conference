from django.db import models
from core.models import BaseModel
from conferences.slug_generate import generate_unique_slug
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class Conference(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    short_name = models.CharField(max_length=100, db_index=True)  # IICSD-2027
    slug = models.SlugField(unique=True)

    location = models.CharField(max_length=255)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    description = models.TextField(blank=True)

    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
        ]
    #slug safe
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, field_name='name')

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            self.slug = generate_unique_slug(self, field_name='name')
            super().save(*args, **kwargs)



class Track(BaseModel):
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name="tracks"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tracks"
    )
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "conference"],
                name="one_track_per_user_per_conference"
            )
        ]





class Session(BaseModel):
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["start_time", "end_time"]),
        ]

    def clean(self):
        # 1. Time validation
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        # 2. Ensure session is inside conference window
        conference = self.track.conference
        if not (conference.start_date <= self.start_time.date() <= conference.end_date):
            raise ValidationError("Session must be within conference dates.")