"""
polls/views.py.

This module contains the views for the polls application. It includes views
for listing questions, displaying details, showing results, and handling votes.

Classes:
- IndexView: Displays a list of the latest questions.
- DetailView: Shows details of a specific question and allows voting.
- ResultsView: Displays the results of a specific question.
- VoteView: Handles voting for a specific choice in a question.
"""

import logging
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from .models import Choice, Question, Vote
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger('myapp')


class IndexView(generic.ListView):
    """
    Display the latest questions.

    Attributes:
        template_name (str): The path to the template that renders the view.
        context_object_name (str): The name of the context variable to use in the template.
    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions, excluding those set to be published in the future.

        Returns:
            QuerySet: A QuerySet of the latest questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    """
    Display details for a specific question and allow voting.

    Attributes:
        model (Question): The model associated with this view.
        template_name (str): The path to the template that renders the view.
    """

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Exclude any questions that aren't published yet.

        Returns:
            QuerySet: A QuerySet of published questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Retrieve the question object and render the template.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponseRedirect: Redirects to the index page if the question is not published.
            HttpResponse: Renders the detail page for the question.
        """
        # Get the question object
        self.object = self.get_object()

        # Check if voting is allowed
        if not self.object.can_vote():
            messages.error(request, "This poll is closed.")
            return redirect('polls:index')

        return self.render_to_response(self.get_context_data(object=self.object))

    def get_context_data(self, **kwargs):
        """
        Add the previous choice of the user to the context data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The updated context data with the previous choice.
        """
        context = super().get_context_data(**kwargs)
        question = self.object
        this_user = self.request.user

        if this_user.is_authenticated:
            try:
                previous_vote = Vote.objects.get(user=this_user, choice__question=question)
                context['previous_choice'] = previous_vote.choice
            except Vote.DoesNotExist:
                context['previous_choice'] = None
        else:
            context['previous_choice'] = None
        return context


class ResultsView(generic.DetailView):
    """
    Display the results for a specific question.

    Attributes:
        model (Question): The model associated with this view.
        template_name (str): The path to the template that renders the view.
    """

    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """
        Retrieve the question and redirect if it is not yet published.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponseRedirect: Redirects to the index page if the question is not published.
            HttpResponse: Renders the results page for the question if it is published.
        """
        question = self.get_object()
        # Check if the question is not published yet
        if question.pub_date > timezone.now():
            # Redirect to the index if the question is not yet published
            return HttpResponseRedirect(reverse('polls:index'))
        # If the question is published, proceed with the default get method
        return super().get(request, *args, **kwargs)


class VoteView(LoginRequiredMixin, View):
    """
    Handle voting for a specific choice in a question.

    Attributes:
        LoginRequiredMixin: Requires the user to be logged in to access this view.
    """

    def post(self, request, question_id):
        """
        Handle the voting process.

        Args:
            request: The HTTP request object.
            question_id: The ID of the question being voted on.

        Returns:
            HttpResponseRedirect: Redirects to the results page or back to the detail page with an error message.
        """
        user = request.user
        question = get_object_or_404(Question, pk=question_id)

        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

        choice_id = request.POST.get("choice")
        if not choice_id:
            messages.error(request, "You didn't select a choice.")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

        try:
            selected_choice = question.choice_set.get(pk=choice_id)
        except Choice.DoesNotExist:
            messages.error(request, "Invalid choice.")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

        existing_vote = Vote.objects.filter(user=user, choice__question=question).first()
        if existing_vote:
            existing_vote.choice = selected_choice
            existing_vote.save()
        else:
            Vote.objects.create(user=user, choice=selected_choice)

        # Log the vote
        logger.info(f"User {user.username} voted for choice {selected_choice.choice_text} in question {question.id}")

        # Add a success message
        messages.success(request, f"Your vote for {selected_choice.choice_text} has been recorded.")

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
