from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    create_time = models.DateTimeField(default=now)

    def __str__(self):
        return self.username