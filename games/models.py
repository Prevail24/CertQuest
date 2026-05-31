"""
games/models.py

This file contains database models related to game modes
available within CertQuest.

Examples:
- Daily Quiz
- Port Matcher
- Subnet Dungeon
- Boss Battle

Each game type can eventually have its own rules,
graphics, XP rewards, and gameplay mechanics.
"""

from django.db import models


class GameType(models.Model):
    """
    Represents a game mode available within CertQuest.

    A GameType defines HOW a user practices a topic,
    while quests define WHAT they are learning.

    Example:
        Topic: OSI Model

        Game Types:
        - Daily Quiz
        - Matching Game
        - Boss Battle
    """

    # Display name shown to users
    name = models.CharField(max_length=100)

    # URL-friendly unique identifier
    # Example: "daily-quiz"
    slug = models.SlugField(unique=True)

    # Description shown in menus or game selection screens
    description = models.TextField()

    # Default XP reward granted for completing the game
    xp_reward = models.IntegerField(default=10)

    # Determines whether the game is available to players
    is_active = models.BooleanField(default=True)

    # Timestamp when the game type was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Human-readable representation shown in Django Admin.
        """
        return self.name