"""
This module defines the models for a simple polling application.
"""
import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    """
    - Question: Represents a poll question, containing the text of the question and the publication date.
        - Methods:
            - __str__(): Returns the question text as a string representation.
            - was_published_recently(): Checks if the question was published within the last day.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Checks if the poll was published recently.
        :return:  boolean
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    - Choice: Represents a possible answer to a poll question, linked to a specific Question.
        - Fields:
            - question: ForeignKey linking to the associated Question.
            - choice_text: Text of the choice.
            - votes: Number of votes this choice has received (default is 0).
        - Methods:
            - __str__(): Returns the choice text as a string representation.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text



