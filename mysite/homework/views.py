from django.shortcuts import render
from django.http import HttpResponse

def index(request, year):
    return HttpResponse("Submit your homework here! % year")

def detail(request, year, homework_id):
    return HttpResponse("Submit your homework here! % year")

def submit(request, year, homework_id):
    return HttpResponse("Submit your homework here! % year")

def result(request, year, homework_id):
    return HttpResponse("Submit your homework here! % year")