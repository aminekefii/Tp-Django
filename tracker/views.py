# tracker/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MoodEntryForm, TagForm
from .models import MoodEntry, Tag


def home(request):
    return render(request, "home.html")


@login_required
def entry_list(request):
    entries = (MoodEntry.objects.filter(user=request.user)
               .select_related("category")
               .prefetch_related("tags")
               .order_by("-created_at"))

    return render(request, "moods/entry_list.html", {
        "entries": entries})


@login_required
def entry_create(request):
    if request.method == "POST":
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            form.save_m2m()
            messages.success(request, "Mood saved.")
            return redirect("entry_list")
    else:
        form = MoodEntryForm()

    return render(request, "moods/entry_form.html",
                  {"form": form})


def entry_detail(request, id):
    return HttpResponse(f"Detail of entry #{id}")


@login_required
def entry_edit(request, id):
    entry = get_object_or_404(
        MoodEntry, pk=id, user=request.user)

    if request.method == "POST":
        form = MoodEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry updated.")
            return redirect("entry_list")
    else:
        form = MoodEntryForm(instance=entry)

    return render(request, "moods/entry_form.html",
                  {"form": form, "object": entry})


def entry_delete(request, id):
    return HttpResponse(f"Confirm deletion of entry #{id}")


@login_required
def tag_list(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, "Tag created.")
            return redirect("tag_list")
    else:
        form = TagForm()

    return render(request, "tags/tag_list.html",
                  {"tags": Tag.objects.all(), "form": form})


@login_required
def tag_edit(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag updated.")
            return redirect("tag_list")
    else:
        form = TagForm(instance=tag)

    return render(request, "tags/tag_list.html",
                  {"tags": Tag.objects.all(),
                   "form": form, "editing": tag})


def tag_detail(request, slug):
    return HttpResponse(f"Entries tagged '{slug}'")


def category_list(request):
    return HttpResponse("List of mood categories")


def stats(request):
    total_entries = 3
    average_mood = 3.6
    average_intensity = 6
    current_streak = 12
    return render(request, "moods/stats.html", {
        "total_entries": total_entries,
        "average_mood": average_mood,
        "average_intensity": average_intensity,
        "current_streak": current_streak,
    })
