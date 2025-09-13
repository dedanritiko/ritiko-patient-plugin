"""
Patient filters for django-filter
"""
import django_filters
from django import forms
from django.db import models

from patients.models.people import Patient, PatientCategory


class PatientFilter(django_filters.FilterSet):
    """Enhanced patient filter with django-filter."""

    name = django_filters.CharFilter(
        method="filter_name",
        label="Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by first or last name...",
            }
        ),
    )

    mrn = django_filters.CharFilter(
        lookup_expr="icontains",
        label="MRN",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by MRN..."}
        ),
    )

    birth_date = django_filters.DateFromToRangeFilter(
        label="Birth Date Range",
        widget=django_filters.widgets.RangeWidget(
            attrs={"class": "form-control", "type": "date"}
        ),
    )

    gender = django_filters.ChoiceFilter(
        choices=[("", "All")] + list(Patient._meta.get_field("gender").choices),
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    is_active = django_filters.BooleanFilter(
        label="Active Only",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    patient_category = django_filters.ModelChoiceFilter(
        queryset=PatientCategory.objects.all(),
        label="Category",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    phone_number = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Phone",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by phone number..."}
        ),
    )

    city = django_filters.CharFilter(
        lookup_expr="icontains",
        label="City",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by city..."}
        ),
    )

    state = django_filters.CharFilter(
        lookup_expr="icontains",
        label="State",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by state..."}
        ),
    )

    zipcode = django_filters.CharFilter(
        lookup_expr="icontains",
        label="ZIP Code",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by ZIP..."}
        ),
    )

    has_care_team = django_filters.BooleanFilter(
        method="filter_has_care_team",
        label="Has Care Team",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    program = django_filters.ChoiceFilter(
        choices=[("", "All")] + list(Patient._meta.get_field("program").choices),
        label="Program",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Patient
        fields = [
            "name",
            "mrn",
            "birth_date",
            "gender",
            "is_active",
            "patient_category",
            "phone_number",
            "city",
            "state",
            "zipcode",
            "has_care_team",
            "program",
        ]

    def filter_name(self, queryset, name, value):
        """Filter by first name or last name."""
        if not value:
            return queryset
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )

    def filter_has_care_team(self, queryset, name, value):
        """Filter patients who have care team members."""
        if value is None:
            return queryset
        if value:
            return queryset.filter(care_team__isnull=False).distinct()
        else:
            return queryset.filter(care_team__isnull=True)


class CompactPatientFilter(django_filters.FilterSet):
    """Compact patient filter for smaller views."""

    name = django_filters.CharFilter(
        method="filter_name",
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm", "placeholder": "Name..."}
        ),
    )

    is_active = django_filters.BooleanFilter(
        label="Active", widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Patient
        fields = ["name", "is_active"]

    def filter_name(self, queryset, name, value):
        """Filter by first name or last name."""
        if not value:
            return queryset
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )
