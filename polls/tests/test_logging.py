# polls/tests.py

from django.test import TestCase, Client
from ..models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import logging

logger = logging.getLogger('myapp')

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

class LoggingTests(TestCase):

    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # Create a test question and choices
        self.question = Question.objects.create(question_text="What's new?", pub_date=timezone.now())
        self.choice = Choice.objects.create(question=self.question, choice_text="Test choice")
        self.client = Client()

    def test_login_logging(self):
        # Perform login
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after login

        # Check the log file for the expected log message
        log_file_path = 'logs/django.log'
        try:
            with open(log_file_path, 'r') as f:
                logs = f.read()
            # Ensure to match the exact log format, adjust if needed
            self.assertIn(f"User {self.username} logged in from IP address", logs)
        except FileNotFoundError:
            self.fail(f"Log file {log_file_path} not found. Ensure logging is configured correctly.")

    def test_logout_logging(self):
        # Log in the user first
        self.client.login(username=self.username, password=self.password)
        # Perform logout
        response = self.client.post(reverse('logout'))  # Ensure POST request without credentials
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after logout

        # Check the log file for the expected log message
        log_file_path = 'logs/django.log'
        try:
            with open(log_file_path, 'r') as f:
                logs = f.read()
            self.assertIn(f"User {self.username} logged out from IP address", logs)
        except FileNotFoundError:
            self.fail(f"Log file {log_file_path} not found. Ensure logging is configured correctly.")
