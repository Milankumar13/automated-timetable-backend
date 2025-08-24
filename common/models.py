import uuid
from django.db import models

class BaseModel(models.Model):
    """Adds UUID and timestamps to every table."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # global unique id
    created_at = models.DateTimeField(auto_now_add=True)  # set on insert
    updated_at = models.DateTimeField(auto_now=True)      # set on update

    class Meta:
        abstract = True
