from datetime import date

from django.db.models import CharField

from django.conf import settings

from shortuuid import ShortUUID

class KIdxField(CharField):
    description = "A custom (short) UUID field."
    alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

    model_prefix = None

    def __init__(self, *args, **kwargs):
        self.length = kwargs.pop("length", 8)

        if "max_length" not in kwargs:
            # If `max_length` was not specified, set it here.
            kwargs["max_length"] = self.length + settings.KIDX_PREFIX_LENGTH + 1 # Prefix Length + 1 separator

        kwargs.update({"unique": True, "editable": False, "blank": True})

        super().__init__(*args, **kwargs)

    def get_model_prefix(instance):
        """Get the model prefix from the model name."""
        model_name = instance._meta.model_name
        model_prefix = settings.KIDX_PREFIXES[model_name]
        if len(model_prefix) != settings.KIDX_PREFIX_LENGTH:
            raise ValueError(
                f"Model prefix for {model_name} must be {settings.KIDX_PREFIX_LENGTH} characters long."
            )

    def _generate_uuid(self, model_prefix):
        """Generate a short random string."""
        _year = str(date.today().year)[2:] # Prefix with two digit year
        _uuid = ShortUUID(alphabet=self.alphabet).random(length=self.length)
        return f"{model_prefix}_{_year}{_uuid}".upper()

    def pre_save(self, instance, add):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """

        value = super().pre_save(instance, add)
        if not value:
            model_prefix = self.get_model_prefix(instance)
            value = self._generate_uuid(model_prefix)
        instance.idx = value
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["length"] = self.length
        kwargs.pop("default", None)
        return name, path, args, kwargs
