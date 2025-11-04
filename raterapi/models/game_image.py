from django.db import models
from django.contrib.auth.models import User


class GameImage(models.Model):
    """Game Image Model"""

    image = models.ImageField(upload_to="../images")
    game = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="game_image"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name=("user_image")
    )
