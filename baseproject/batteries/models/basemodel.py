from django.db import models

from .kidx_field import KIdxField

class BaseModel(models.Model):
    idx = KIdxField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Redundant field, but if you want the speed up some queries, you can use this though redundant. 
    created_date = models.DateField(auto_now_add=True)

    # For Soft Delete. If you don't want to use this, you should remove this from your model.
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    """

    class Meta:
        abstract = True