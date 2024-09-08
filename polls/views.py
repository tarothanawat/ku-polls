from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from .models import Choice, Question, Vote
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin



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
        # Check if the question is not published yet
        if question.pub_date > timezone.now():
            # Redirect to the index if the question is not yet published
            return HttpResponseRedirect(reverse('polls:index'))
        # If the question is published, proceed with the default get method
        return super().get(request, *args, **kwargs)


class VoteView(LoginRequiredMixin, View):
    """
    Handles voting for a specific choice in a question.
    """

    def post(self, request, question_id):
        user = request.user
        question = get_object_or_404(Question, pk=question_id)

        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

        choice_id = request.POST.get("choice")
        if not choice_id:
            # Handle the case where no choice is selected
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )

        try:
            selected_choice = question.choice_set.get(pk=choice_id)
        except Choice.DoesNotExist:
            # Handle the case where the choice is invalid
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Invalid choice.",
                },
            )

        existing_vote = Vote.objects.filter(user=user, choice__question=question).first()
        if existing_vote:
            existing_vote.choice = selected_choice
            existing_vote.save()
        else:
            Vote.objects.create(user=user, choice=selected_choice)

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
