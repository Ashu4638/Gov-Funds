from django.db import models

# Create your models here.
class Wallets(models.Model):
    username = models.TextField(primary_key=True)
    balance = models.IntegerField()


class History(models.Model):
    ID = models.IntegerField(auto_created=True, primary_key=True)
    fromAdd = models.TextField()
    toAdd = models.TextField()
    amount = models.IntegerField()
    timestamp = models.TextField()
    status = models.TextField()


