from django.db import models
from baseproject.batteries.models import BaseModel

class Role(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    permission = models.ManyToManyField('Permission', through='RolePermission')

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name
    

class Permission(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name
    
class RolePermission(BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"