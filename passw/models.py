from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name_service = models.CharField(max_length=50)
    username_service = models.CharField(max_length = 50)
    password_service = models.CharField(max_length = 50)

    def __str__(self)->str:
        return self.name_service