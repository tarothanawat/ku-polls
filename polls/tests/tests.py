from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question
from django.urls import reverse


# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
                was_published_recently() returns False for questions whose pub_date
                is in the future.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def setUp(self):
        """
        Create sample questions for testing.
        """
        self.now = timezone.now()
        self.future_date = self.now + datetime.timedelta(days=30)
        self.past_date = self.now - datetime.timedelta(days=30)

        # Create questions for each test case
        self.future_question = Question.objects.create(
            question_text="Future question",
            pub_date=self.future_date
        )
        self.default_question = Question.objects.create(
            question_text="Default question",
            pub_date=self.now
        )
        self.past_question = Question.objects.create(
            question_text="Past question",
            pub_date=self.past_date
        )

    def test_question_with_future_pub_date(self):
        """
        Question with a future publication date should not be considered published.
        """
        self.assertFalse(self.future_question.is_published())

    def test_question_with_default_pub_date(self):
        """
        Question with the default publication date (now) should be considered published.
        """
        self.assertTrue(self.default_question.is_published())

    def test_question_with_past_pub_date(self):
        """
        Question with a publication date in the past should be considered published.
        """
        self.assertTrue(self.past_question.is_published())

    def test_can_vote_before_end_date(self):
        """
        Voting should be allowed if the current date is between pub_date and end_date.
        """
        # Set up a question with an end_date in the future
        future_end_date = timezone.localtime() + datetime.timedelta(days=30)
        question = Question.objects.create(
            question_text="Question with future end_date",
            pub_date=timezone.localtime() - datetime.timedelta(days=1),
            end_date=future_end_date
        )
        self.assertTrue(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        Voting should not be allowed if the current date is after end_date.
        """
        # Set up a question with an end_date in the past
        past_end_date = timezone.localtime() - datetime.timedelta(days=1)
        question = Question.objects.create(
            question_text="Question with past end_date",
            pub_date=timezone.localtime() - datetime.timedelta(days=10),
            end_date=past_end_date
        )
        self.assertFalse(question.can_vote())

    def test_can_vote_when_end_date_is_null(self):
        """
        Voting should be allowed if end_date is null and the current date is after pub_date.
        """
        # Set up a question with end_date as null
        question = Question.objects.create(
            question_text="Question with no end_date",
            pub_date=timezone.localtime() - datetime.timedelta(days=1),
            end_date=None
        )
        self.assertTrue(question.can_vote())


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + timezone.timedelta(days=30)
        )
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, future_question.question_text)
        self.assertContains(response, "No polls are available.")

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


