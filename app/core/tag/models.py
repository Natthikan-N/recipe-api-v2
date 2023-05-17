from django.db import models
from app.settings import AUTH_USER_MODEL

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=225)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    