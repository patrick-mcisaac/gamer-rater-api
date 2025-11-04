from django.db import models
from django.contrib.auth.models import User


class Rating(models.Model):
    """rating model"""

    rating = models.IntegerField()
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="rated_game")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating_user")
