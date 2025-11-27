from django.shortcuts import render
from django.http import HttpResponse

def sign_up(request):
    return render(request,"users/sign_up.html")

def sign_in(request):
    return render(request,"users/sign_in.html")