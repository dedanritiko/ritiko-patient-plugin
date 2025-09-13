"""
Patient plugin views with django-tables2 and django-filter
"""

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import OuterRef, Prefetch, Subquery
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django_tables2.export import ExportMixin

from core.views.utils import RitikoViewMixin
from patients.models import Insurance, Intake, ReferralNote
from patients.models.people import Patient

from .filters import CompactPatientFilter, PatientFilter
from .tables import CompactPatientTable, PatientTable


class PatientListView(
    RitikoViewMixin, PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView
):
    """Enhanced patient list view with tables and filters."""

    model = Patient
    table_class = PatientTable
    filterset_class = PatientFilter
    template_name = "patient_plugin/patient_list.html"
    context_object_name = "patients"
    permission_required = "patient_plugin.can_view_patient_list"
    export_formats = ["csv", "xlsx", "json"]

    @property
    def title(self):
        return _("Patients List")

    def get_queryset(self):
        """Get patients for current organization - patients with intake and no discharge."""
        return (
            Patient.objects.filter(
                organization=self.request.user.organization,
                is_active=True,
                intake_complete=True,
            )
            .annotate(
                latest_date_of_admission=Subquery(
                    Intake.objects.filter(patient=OuterRef("pk"))
                    .order_by("-created_on")
                    .only("date_of_admission")
                    .values("date_of_admission")[:1]
                ),
                latest_referral_note=Subquery(
                    ReferralNote.objects.filter(patient=OuterRef("pk"))
                    .order_by("-created_on")
                    .values("note")[:1]
                ),
            )
            .select_related("organization", "patient_category")
            .prefetch_related(
                "care_team",
                Prefetch(
                    "insurance_set",
                    queryset=Insurance.objects.filter(
                        insurance_type=Insurance.PRIMARY
                    ).only(
                        "id", "patient_id", "insurance_type", "provider", "id_number"
                    ),
                    to_attr="prefetched_primary_insurance_list",
                ),
            )
        )

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        return context

    def get_paginate_by(self, queryset):
        """Override paginate_by to handle per_page parameter."""
        per_page = self.request.GET.get("per_page", "20")
        try:
            per_page = int(per_page)
            if per_page in [5, 10, 20, 50, 100, 200]:
                return per_page
            else:
                return 20
        except (ValueError, TypeError):
            return 20


class CompactPatientListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    """Compact patient list view for smaller displays."""

    model = Patient
    table_class = CompactPatientTable
    filterset_class = CompactPatientFilter
    template_name = "patient_plugin/compact_patient_list.html"
    context_object_name = "patients"
    permission_required = "patient_plugin.can_view_patient_list"

    def get_queryset(self):
        """Get patients for current organization."""
        return Patient.objects.filter(
            organization=self.request.user.organization
        ).select_related("organization")


def patient_stats_view(request):
    """Simple view for patient statistics."""
    if not request.user.has_perm("patient_plugin.can_view_patient_list"):
        return HttpResponse("Permission denied", status=403)

    patients = Patient.objects.filter(organization=request.user.organization)

    stats = {
        "total": patients.count(),
        "active": patients.filter(is_active=True).count(),
        "inactive": patients.filter(is_active=False).count(),
        "with_care_team": patients.filter(care_team__isnull=False).distinct().count(),
        "by_gender": {
            gender[0]: patients.filter(gender=gender[0]).count()
            for gender in Patient._meta.get_field("gender").choices
        },
    }

    return render(request, "patient_plugin/patient_stats.html", {"stats": stats})
