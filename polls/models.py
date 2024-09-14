"""This module defines the models for a simple polling application."""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Represents a question in the poll.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """Return the string representation of the question."""
        return self.question_text

    def was_published_recently(self):
        """
        Return whether the question was published recently (within the last day).

        Returns:
            bool: True if published within the last day, otherwise False.
        """
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)

    def can_vote(self):
        """
        Determine if voting is allowed for this question.

        Returns:
            bool: True if voting is allowed, otherwise False.
        """
        return self.pub_date <= timezone.now()


class Choice(models.Model):
    """
    Represents a choice for a question in the poll.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the string representation of the choice."""
        return self.choice_text


class Vote(models.Model):
    """
    Represents a vote cast by a user for a choice in a question.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    date_voted = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Vote model."""
        unique_together = ('user', 'choice')

    def __str__(self):
        """Return the string representation of the vote."""
        return f"{self.user.username} voted for {self.choice.choice_text} on {self.date_voted}"