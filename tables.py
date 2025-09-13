"""
Patient tables for django-tables2
"""
import django_tables2 as tables

from patients.models.people import Patient


class PatientTable(tables.Table):
    """Enhanced patient table matching the original patients table style."""

    actions = tables.TemplateColumn(
        template_name="patient_plugin/columns/actions_column_enhanced.html",
        verbose_name="Actions",
        orderable=False,
        attrs={"td": {"class": "text-center"}, "th": {"scope": "col"}},
    )

    mrn = tables.Column(
        verbose_name="MRN", attrs={"th": {"scope": "col"}}, accessor="mrn", default="-"
    )

    last_name = tables.TemplateColumn(
        template_name="patient_plugin/columns/name_column.html",
        verbose_name="Last Name",
        orderable=True,
        attrs={"th": {"scope": "col"}},
    )

    middle_name = tables.TemplateColumn(
        template_name="patient_plugin/columns/middle_name_column.html",
        verbose_name="Middle Name",
        orderable=True,
        attrs={"th": {"scope": "col"}},
    )

    first_name = tables.TemplateColumn(
        template_name="patient_plugin/columns/first_name_column.html",
        verbose_name="First Name",
        orderable=True,
        attrs={"th": {"scope": "col"}},
    )

    gender = tables.Column(
        verbose_name="Gender",
        accessor="get_gender_display",
        attrs={"th": {"scope": "col"}},
    )

    patient_category = tables.Column(
        verbose_name="Category",
        accessor="patient_category.name",
        default="-",
        attrs={"td": {"class": "text-center"}, "th": {"scope": "col"}},
    )

    eligible_insurance = tables.Column(
        verbose_name="Eligible Insurance",
        accessor="get_primary_insurance.provider",
        default="-",
        attrs={"td": {"class": "text-center"}, "th": {"scope": "col"}},
    )

    evv_ready = tables.TemplateColumn(
        template_name="patient_plugin/columns/evv_ready_column.html",
        verbose_name="EVV Ready",
        accessor="is_evv_ready",
        orderable=True,
        attrs={"td": {"class": "text-center"}, "th": {"scope": "col"}},
    )

    program = tables.TemplateColumn(
        template_name="patient_plugin/columns/program_column.html",
        verbose_name="Program",
        orderable=True,
        attrs={"td": {"class": "text-center"}, "th": {"scope": "col"}},
    )

    admission_date = tables.DateColumn(
        verbose_name="Admission Date",
        accessor="latest_date_of_admission",
        format="m/d/Y",
        default="-",
        attrs={"td": {"class": "text-center"}, "th": {"scope": "col"}},
    )

    class Meta:
        model = Patient
        template_name = "patient_plugin/custom_table.html"
        fields = (
            "actions",
            "mrn",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "eligible_insurance",
            "evv_ready",
            "patient_category",
            "program",
            "admission_date",
        )
        attrs = {"class": "table table-hover", "width": "100%"}


class CompactPatientTable(tables.Table):
    """Compact patient table for smaller views."""

    name = tables.Column(verbose_name="Name", accessor="get_full_name")

    mrn = tables.Column(verbose_name="MRN")

    birth_date = tables.DateColumn(format="m/d/Y", verbose_name="DOB")

    is_active = tables.BooleanColumn(verbose_name="Active", yesno="✓,✗")

    class Meta:
        model = Patient
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "mrn", "birth_date", "is_active")
        attrs = {
            "class": "table table-sm table-striped",
            "thead": {"class": "table-dark"},
        }
        per_page = 50
