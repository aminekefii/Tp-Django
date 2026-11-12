# authentication/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect


def signup(request):
    return render(request, "registration/signup.html")


def login_view(request):
    return render(request, "registration/login.html")


def logout_view(request):
    return redirect("login")


def profile(request):
    return render(request, "accounts/profile.html")


def delete_profile(request):
    return redirect("login")
