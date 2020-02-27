from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):

    """this creates instances of customers
                    Matt Blagg wuz here """

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    # is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        """ordering = order of how data is presented"""

        ordering = (F('user.date_joined').asc(nulls_last=True),)
        ordering = ("created_at",)
