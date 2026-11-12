# authentication/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import LoginForm, SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("entry_create")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    next_url = (request.POST.get("next")
                or request.GET.get("next") or "")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = LoginForm(request)
    return render(request, "registration/login.html",
                  {"form": form, "next": next_url})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("login")


def profile(request):
    return render(request, "accounts/profile.html")


def delete_profile(request):
    return redirect("login")
