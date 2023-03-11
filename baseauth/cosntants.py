from django.db import models

class GenderType(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHERS = "others", "Others"
    UNKNOWN = "unknown", "Unknown"

class UserAttributeType(models.TextChoices):
    PHONE = "phone", "Phone"
    EMAIL = "email", "Email"
    ADDRESS = "address", "Address"
    CITY = "city", "City"
    STATE = "state", "State"
    COUNTRY = "country", "Country"
    ZIP_CODE = "zip_code", "Zip Code"