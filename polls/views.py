from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from .models import Choice, Question
from django.contrib import messages


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        # Use the is_published method to filter questions
        return [q for q in Question.objects.all().order_by("-pub_date") if q.is_published()][:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        # Use the is_published method to filter questions
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Override the get method to check if voting is allowed.
        """
        question = self.get_object()
        if not question.can_vote():
            messages.error(request, "Voting is not allowed for this poll.")
            return redirect(reverse('polls:index'))

        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class VoteView(View):
    """
    Handles voting for a specific choice in a question.
    """

    def post(self, request, question_id):
        # Retrieve the question object
        question = get_object_or_404(Question, pk=question_id)

        # Use the can_vote method to check if voting is allowed
        if not question.can_vote():
            # If voting is not allowed, show an error message on the detail page
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "Voting is not allowed for this question.",
                },
            )

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
        else:
            # Use F() expression to avoid race conditions
            selected_choice.votes = F("votes") + 1
            selected_choice.save()

            # Redirect to the results page after successful vote to prevent multiple submissions
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
