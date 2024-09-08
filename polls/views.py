from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from .models import Choice, Question, Vote
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return redirect(reverse('polls:index'))

        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        if question.pub_date > timezone.now():
            return HttpResponseRedirect(reverse('polls:index'))
        return super().get(request, *args, **kwargs)


class VoteView(LoginRequiredMixin, View):
    """
    Handles voting for a specific choice in a question.
    """

    def post(self, request, question_id):
        # Retrieve the logged-in user
        user = request.user

        # Retrieve the question object
        question = get_object_or_404(Question, pk=question_id)

        # Use the can_vote method to check if voting is allowed
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

        try:
            # Get the selected choice from the form data (POST request)
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # If no choice was selected or choice does not exist, re-render the form with an error message
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )

        # Check if the user has already voted for this question
        existing_vote = Vote.objects.filter(user=user, choice__question=question).first()
        if existing_vote:
            # If an existing vote is found, update it
            existing_vote.choice = selected_choice
            existing_vote.save()
        else:
            # Create a new vote
            Vote.objects.create(user=user, choice=selected_choice)

        # Redirect to the results page after successful vote to prevent multiple submissions
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
