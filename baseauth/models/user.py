from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from baseproject.batteries.models import BaseModel

from ..cosntants import GenderType, UserAttributeType
from ..models.role import Role

from django.utils.translation import gettext as _t

"""
The User Model
"""
class User(AbstractBaseUser, BaseModel):
    first_name = models.CharField(_t("First Name"), max_length=127)
    last_name = models.CharField(_t("Last Name"), max_length=127)
    gender = models.CharField(
        max_length=20, choices=GenderType.choices, default=GenderType.UNKNOWN
    )
    email = models.EmailField(("Email Address"), unique=True)
    is_verified = models.BooleanField(
        _t("Verified"),
        default=False,
        help_text="Email verification status",
    )
    last_login = models.DateTimeField(blank=True, null=True) # To be updated during login actions only
    email_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to="profile/", blank=True, null=True, max_length=255
    )
    roles = models.ManyToManyField(Role, related_name="roles")

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    ordering = ("created_at",)

    @property
    def _get_roles(self):
        return self.roles.all()

    @property
    def _get_all_permissions(self):
        return [i.permissions for i in self.roles.all()]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        unique_together = ("email", "deleted_at") # Allowing same email to create new account in case of soft delete

    def __str__(self):
        return f"{self.email}"


"""
The OneToMany Model for User attributes
Usage : create a bucket for 
"""
class UserAttribute(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attribute_bucket = models.CharField(max_length=100, default="default")
    attribute_type = models.CharField(max_length=15, choices=UserAttributeType.choices)
    value = models.CharField(max_length=100, blank=True, null=True)
    value_json = models.JSONField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Attribute"
        verbose_name_plural = "User Attributes"
        unique_together = (
            ("user", "attribute_bucket"),  # Can have several unique bucket types
            ("user", "attribute_bucket", "attribute_type"),  # one user bucket can have unique attributes by type 
        )

    def __str__(self):
        return self.user.email
