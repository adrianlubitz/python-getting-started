from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class Suggestion(models.Model):
    color = models.CharField(max_length=100)
    describtion = models.CharField(max_length=100)
    author = models.CharField(max_length=100, primary_key=True)

class Draw(models.Model):
    color = models.CharField(max_length=100)
    describtion = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    giver = models.CharField(max_length=100, primary_key=True)

    class Meta:
        unique_together = (('recipient', 'giver'))