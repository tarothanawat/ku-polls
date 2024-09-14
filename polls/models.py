"""
This module defines the models for a simple polling application.
"""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    """
    Represents a poll question, containing the text of the question and the publication date.

    Attributes:
        question_text (str): The text of the poll question.
        pub_date (datetime): The publication date of the question.
        end_date (datetime): The end date for voting. If null, voting is allowed anytime after pub_date.

    Methods:
        __str__(): Returns the question text as a string representation.
        was_published_recently(): Checks if the question was published within the last day.
        is_published(): Returns True if the current date-time is on or after the question's publication date.
        can_vote(): Returns True if voting is allowed for this question.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def __str__(self):
        """Returns the question text as a string representation."""
        return self.question_text

    def was_published_recently(self):
        """
        Checks if the poll was published recently.

        Returns:
            bool: True if the question was published within the last day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Returns True if the current local date-time is on or after the question's publication date.

        Returns:
            bool: True if the question is published.
        """
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """
        Returns True if voting is allowed for this question.

        Voting is allowed if:
            - Current local date-time is after or on the pub_date.
            - Current local date-time is before the end_date, if end_date is not None.

        Returns:
            bool: True if voting is allowed.
        """
        now = timezone.now()
        if self.end_date:
            return self.pub_date <= now <= self.end_date
        return now >= self.pub_date


class Choice(models.Model):
    """
    Represents a choice for a given question in the poll.

    Attributes:
        question (Question): The question to which this choice belongs.
        choice_text (str): The text of the choice.
        votes (int): The number of votes for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Returns the choice text as a string representation."""
        return self.choice_text

    @property
    def vote_count(self):
        """
        Returns the number of votes for this choice.

        Returns:
            int: Number of votes for this choice.
        """
        return self.vote_set.count()


class Vote(models.Model):
    """
    Records a choice for a question made by a user.

    Attributes:
        user (User): The user who made the vote.
        choice (Choice): The choice that was voted for.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation of the vote."""
        return f"{self.user.username} voted for {self.choice.choice_text}"
