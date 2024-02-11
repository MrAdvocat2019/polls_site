import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    text=models.CharField(max_length=200)
    productiondate=models.DateTimeField("date published")

    def was_published_recently(self):
        return self.productiondate >= timezone.now() - datetime.timedelta(days=1) and self.productiondate<timezone.now()
    def __str__(self):
        return self.text
    class Meta:
        permissions=(("can_nullify","User can nullify votes" ),)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def votesx2(self):
        return self.votes*2
    def __str__(self):
        return self.choice_text
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text
