import csv

from django.contrib.admin import ModelAdmin
from django.db import models
from django.db.models import DateTimeField
from django.forms import SplitDateTimeWidget
from django.utils import timezone
from django_json_widget.widgets import JSONEditorWidget

from .filters import DateFilter, EndDateFilter, StartDateFilter

class BaseBatteryModelAdmin(ModelAdmin):
    use_date_range = False
    show_date_filter = False
    possible_readonly_fields = ["created_on", "modified_on", "deleted_on"]
    possible_raw_id_fields = [
        "product",
    ]

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.raw_id_fields = self.get_raw_id_fields(model)

    def get_readonly_fields(self, request, obj):
        readonly_fields = list(self.readonly_fields)
        for x in filter(lambda x: hasattr(obj, x), self.possible_readonly_fields):
            readonly_fields.append(x)
        return list(set(readonly_fields))

    def get_raw_id_fields(self, model):
        raw_id_fields = list(self.raw_id_fields)
        for x in filter(lambda x: hasattr(model, x), self.possible_raw_id_fields):
            raw_id_fields.append(x)
        return list(set(raw_id_fields))

    def get_exclude(self, request, obj):
        return self.possible_readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            if hasattr(obj, "created_by_id") and obj.created_by_id is None:
                obj.created_by_id = request.user.id
            if hasattr(obj, "performed_by_id") and obj.performed_by_id is None:
                obj.performed_by_id = request.user.id

        if obj.is_obsolete is True and any(
            [obj.deleted_on is None, obj.is_obsolete == ""]
        ):
            obj.deleted_on = timezone.now()
        obj.save()

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
        DateTimeField: {
            "widget": SplitDateTimeWidget(
                date_attrs={
                    "type": "date",
                    "class": "vDateField mr-2",
                },
                time_attrs={"type": "time", "class": "vTimeField"},
            )
        },
    }

    def get_list_filter(self, request):
        if self.show_date_filter:
            if self.use_date_range:
                filter_list = (StartDateFilter, EndDateFilter)
            else:
                filter_list = (DateFilter,)
        else:
            filter_list = ()
        return list(super(BaseBatteryModelAdmin, self).get_list_filter(request)) + list(
            filter_list
        )

    list_per_page = 50


class BaseBatteryReadonlyAdmin(BaseBatteryModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class BaseBatteryCreateOnlyAdmin(BaseBatteryModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
