from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.conf import settings

class User(AbstractUser):
    pass

    def __str__(self):
        return f"Username: {self.username}"

