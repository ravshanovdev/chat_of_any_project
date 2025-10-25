from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    ("expert", "Expert"),
    ("farmer", "Farmer")
)


class CustomUser(AbstractUser):
    role = models.CharField(max_length=150, choices=ROLE_CHOICES)

    def __str__(self):
        return f"username: {self.username} <---> role: {self.role}"

