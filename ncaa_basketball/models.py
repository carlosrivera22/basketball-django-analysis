from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=200)
    conference = models.CharField(max_length=200)
    total_games = models.PositiveIntegerField()
    games_won = models.PositiveIntegerField()
    games_lost = models.PositiveIntegerField()
    win_pct = models.FloatField()
    offensive_efficiency = models.FloatField()
    defensive_efficiency = models.FloatField()

    def __str__(self):
        return str(self.name)

   


    



