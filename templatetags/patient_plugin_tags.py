"""
Template tags for patient plugin
"""
from django import template

register = template.Library()


@register.filter
def user_in_care_team(patient, user):
    """Check if user is in patient's care team."""
    if hasattr(patient, "care_team") and user.is_authenticated:
        return patient.care_team.filter(id=user.id).exists()
    return False
