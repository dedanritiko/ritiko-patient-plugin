"""
Patient plugin URL configuration
"""
from django.urls import path

from . import views

app_name = "patient_plugin"

urlpatterns = [
    path("patients/", views.PatientListView.as_view(), name="patient_list"),
    path(
        "patients/compact/",
        views.CompactPatientListView.as_view(),
        name="compact_patient_list",
    ),
    path("patients/stats/", views.patient_stats_view, name="patient_stats"),
]

# Define URL overrides - these will be prepended to the original patients URLs
# Only override the specific URLs we want to change
URL_OVERRIDES = {
    "patients/": [
        # Override the main patient list view (empty path)
        path("", views.PatientListView.as_view(), name="list"),
        # Add new plugin-specific URLs
    ]
}
