from django.db import models


class Category(models.Model):
    """Category model"""

    name = models.CharField(max_length=150)
