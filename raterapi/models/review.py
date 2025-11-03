from django.db import models

from django.contrib.auth.models import User


class Review(models.Model):
    """Review Model"""

    review = models.CharField(max_length=300)
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="game_review"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_review")
