from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ticker(models.Model):
    
    user      = models.ForeignKey(User, verbose_name='subs_user', on_delete=models.CASCADE)
    email     = models.EmailField(max_length=254, blank=True)
    symbol    = models.CharField(max_length=10, blank=True)
    max_price = models.CharField(max_length=10, blank=True)
    min_price = models.CharField(max_length=10, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol
