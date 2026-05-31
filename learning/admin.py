"""
learning/admin.py

Registers learning-related models so they can be managed
through the Django admin panel.
"""

from django.contrib import admin
from .models import CertificationPath
from .models import CertificationPath, Domain

admin.site.register(Domain)
admin.site.register(CertificationPath)