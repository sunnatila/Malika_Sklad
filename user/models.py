from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(unique=True, null=True, blank=True, max_length=50)
    tg_id = models.CharField(null=True, blank=True, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=50)
    first_name = models.CharField(null=True, blank=True, max_length=50)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'