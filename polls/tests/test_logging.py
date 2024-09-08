# polls/tests.py

from django.test import TestCase, Client
from ..models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.utils import timezone

class VoteLoggingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.question = Question.objects.create(question_text="Sample Question", pub_date=timezone.now())
        self.choice = Choice.objects.create(question=self.question, choice_text="Choice 1")

    def test_vote_logging(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(f'/polls/{self.question.id}/vote/', {'choice': self.choice.id})
        with open('logs/django.log', 'r') as f:
            logs = f.read()
        self.assertIn(f"User testuser voted for choice Choice 1 in question {self.question.id}", logs)
