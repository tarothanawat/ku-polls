from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Question, Choice, Vote


class VoteViewTests(TestCase):
    def setUp(self):
        """Set up a user, a question, and choices for testing."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.question = Question.objects.create(
            question_text='Test Question',
            pub_date=timezone.now()
        )
        self.choice1 = Choice.objects.create(question=self.question, choice_text='Choice 1')
        self.choice2 = Choice.objects.create(question=self.question, choice_text='Choice 2')

    def test_vote_successful(self):
        """Test that a user can vote for a choice."""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('polls:vote', args=[self.question.id]), {'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302)  # Redirects to results page
        self.assertEqual(Vote.objects.count(), 1)
        self.assertTrue(Vote.objects.filter(user=self.user, choice=self.choice1).exists())

    def test_update_vote(self):
        """Test that a user's vote is updated if they vote again for the same question."""
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('polls:vote', args=[self.question.id]), {'choice': self.choice1.id})
        self.client.post(reverse('polls:vote', args=[self.question.id]), {'choice': self.choice2.id})
        self.assertEqual(Vote.objects.count(), 1)
        self.assertTrue(Vote.objects.filter(user=self.user, choice=self.choice2).exists())
        self.assertFalse(Vote.objects.filter(user=self.user, choice=self.choice1).exists())

    # def test_no_choice_selected(self):
    #     question = Question.objects.create(question_text='Test Question', pub_date=timezone.now())
    #     Choice.objects.create(question=question, choice_text='Choice 1')
    #
    #     # Simulate POST request with no choice selected
    #     response = self.client.post(reverse('polls:vote', args=(question.id,)), {})
    #
    #     # Follow the redirect to the detail page
    #     response = self.client.get(response.url)
    #
    #     # Check for error message
    #     self.assertContains(response, "You didn't select a choice.")
    #
    # def test_invalid_choice(self):
    #     question = Question.objects.create(question_text='Test Question', pub_date=timezone.now())
    #     Choice.objects.create(question=question, choice_text='Choice 1')
    #
    #     # Simulate POST request with an invalid choice ID
    #     response = self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': 999})
    #
    #     # Follow the redirect to the detail page
    #     response = self.client.get(response.url)
    #
    #     # Check for error message
    #     self.assertContains(response, "Invalid choice.")
