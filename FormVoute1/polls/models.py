import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)

    #date_published is defined as a extra name for database to make code clear
    publication_date = models.DateTimeField('date_published')
    def was_published_recently(self):
        return self.publication_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.question_text

class customChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes_num = models.ImageField(default=0)
    def __str__(self):
        return self.choice_text