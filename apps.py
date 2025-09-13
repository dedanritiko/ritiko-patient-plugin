from core.plugin_app_config import PluginAppConfig


class PatientPluginConfig(PluginAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugins.patient_plugin"
    verbose_name = "Patient Plugin"
