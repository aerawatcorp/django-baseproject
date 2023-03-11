# Model Batteries
Some helpful batteries for the model constructions with default fields for any new models to be created in the project

## BaseModel
```
class BaseModel(models.Model):
    idx = KIdxField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Sometimes you want to update the record without affecting the updated_at field, 
    # however in such case its suggested to handle with other audit log fields
    updated_at = models.DateTimeField(auto_now=True)

    # Redundant field, but if you want the speed up some queries, you can use this though redundant.
    created_date = models.DateField(auto_now_add=True)

    # For Soft Delete. If you don't want to use this, you should remove this from your model.
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # For temporary suspension of any record
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True
```
