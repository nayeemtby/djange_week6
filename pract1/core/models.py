from django.db import models

# Create your models here.


class BankMeta(models.Model):
    is_bankrupt = models.BooleanField(default=False)
