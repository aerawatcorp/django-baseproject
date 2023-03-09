
from datetime import datetime

from django.contrib import admin
from django.db import models
# from django_filters.filters import ModelChoiceFilter
# from django_filters.filterset import (FILTER_FOR_DBFIELD_DEFAULTS, FilterSet,
                                    #   remote_queryset)
# from django_filters.rest_framework import DjangoFilterBackend

YY_MM_DD = "%Y-%m-%d"

class InputFilter(admin.SimpleListFilter):
    template = "admin/input_filter.html"

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice["query_parts"] = (
            (k, v) for k, v in changelist.get_filters_params().items() if k != self.parameter_name
        )
        yield all_choice

    def queryset_with_date_filter(self, request, queryset, date_filter_key):
        if self.value():
            try:
                datevalue = datetime.strptime(self.value(), YY_MM_DD).date()
            except ValueError:
                return queryset.none()
            return queryset.filter({f"{date_filter_key}" : datevalue})



class StartDateFilter(InputFilter):
    parameter_name = "created_on__date__gte"
    title = "Start Date"

    def queryset(self, request, queryset):
        return self.queryset_with_date_filter(request, queryset, self.parameter_name)


class EndDateFilter(InputFilter):
    parameter_name = "created_on__date__lte"
    title = "End Date"

    def queryset(self, request, queryset):
        return self.queryset_with_date_filter(request, queryset, self.parameter_name)


class DateFilter(InputFilter):
    parameter_name = "created_on__date"
    title = "Created on"

    def queryset(self, request, queryset):
        return self.queryset_with_date_filter(request, queryset, self.parameter_name)
