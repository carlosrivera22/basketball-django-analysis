from django.db import models

# Create your models here.
class Shot(models.Model):
    name = models.CharField(max_length=200)
    loc_x = models.FloatField()
    loc_y = models.FloatField()
    made = models.BooleanField(default=True)
    opponent = models.CharField(max_length=200,default='unspecified')
    shot_type = models.CharField(max_length=200,default='unspecified')
    shot_zone = models.CharField(max_length=200,default='unspecified')
    action_type = models.CharField(max_length=200,default='unspecified')

    def __str__(self):
        return str(self.name)


