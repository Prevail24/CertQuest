"""
learning/admin.py

Registers learning-related models so they can be managed
through the Django admin panel.
"""

from django.contrib import admin
from .models import CertificationPath


admin.site.register(CertificationPath)