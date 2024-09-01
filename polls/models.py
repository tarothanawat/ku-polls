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
        - Attributes:
            - question_text: The text of the poll question.
            - pub_date: The publication date of the question.
            - end_date: The end date for voting. If null, voting is allowed anytime after pub_date.
        - Methods:
            - __str__(): Returns the question text as a string representation.
            - was_published_recently(): Checks if the question was published within the last day.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Checks if the poll was published recently.
        :return:  boolean
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Returns True if the current local date-time is on or after the question's publication date.
        :return: boolean
        """
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        """
                Returns True if voting is allowed for this question.
                Voting is allowed if:
                  - Current local date-time is after or on the pub_date.
                  - Current local date-time is before the end_date, if end_date is not None.
                :return: boolean
        """
        now = timezone.localtime()
        if self.end_date:
            return self.pub_date <= now <= self.end_date
        return now >= self.pub_date


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



