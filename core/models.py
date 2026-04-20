from django.db import models
import uuid


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class DeleteObjectsManager(models.Manager):
    """Return all objects including soft deleted"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = ActiveManager()
    all_objects = models.Manager()
    deleted_objects = DeleteObjectsManager() # only deleted

    
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def hard_delete(self,*args, **kwargs):
        super().delete(*args, **kwargs)

    def restore(self):
        self.is_deleted = False
        self.save()

    