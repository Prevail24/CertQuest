from django.contrib import admin
from .models import GameType

# Register your models here.
"""
games/admin.py

Registers game-related models so they can be managed
from the Django admin dashboard.
"""

admin.site.register(GameType)