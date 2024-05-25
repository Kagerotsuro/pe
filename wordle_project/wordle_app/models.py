from django.db import models

class Game(models.Model):
    word = models.CharField(max_length=5)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Attempt(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess = models.CharField(max_length=5)
    colors = models.CharField(max_length=5)  # Stores color information for each letter
    created_at = models.DateTimeField(auto_now_add=True)
