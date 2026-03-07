from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):

    class UserTypeChoice(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Mijoz'
        OPERATOR = 'operator', 'Operator'

    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    banner = models.ImageField(upload_to='banner/', blank=True, null=True)
    intro = models.CharField(max_length=500, blank=True, null=True)
    user_type = models.CharField(
        max_length=30,
        choices=UserTypeChoice.choices,
        default=UserTypeChoice.CLIENT
    )

    def __str__(self):
        return self.username
    

    @property
    def full_name(self):
        return f"{self.first_name} - {self.last_name}"


