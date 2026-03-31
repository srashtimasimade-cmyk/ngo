"""
App configuration for NGO Better Tomorrow.
"""

from django.apps import AppConfig


class NgoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ngo_app'
    verbose_name = 'NGO Better Tomorrow'
