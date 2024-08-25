from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    response = "You're looking at the results of questions %s."
    return HttpResponse(response % question_id)


# def vote(request, question_id):
#     return Http