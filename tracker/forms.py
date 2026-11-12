from django import forms
from django.utils.text import slugify

from .models import MoodEntry, Tag


class MoodEntryForm(forms.ModelForm):
    intensity = forms.IntegerField(
        min_value=1, max_value=10, initial=5)
    note = forms.CharField(
        required=False, max_length=500,
        widget=forms.Textarea(attrs={"rows": 4}))

    class Meta:
        model = MoodEntry
        fields = ["mood", "intensity", "note", "tags"]
        widgets = {
            "mood": forms.RadioSelect,
            "tags": forms.CheckboxSelectMultiple,
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]       # the slug is generated

    def clean_name(self):
        name = self.cleaned_data["name"].strip().lower()
        dup = Tag.objects.filter(name__iexact=name)
        if self.instance.pk:    # editing: ignore itself
            dup = dup.exclude(pk=self.instance.pk)
        if dup.exists():
            raise forms.ValidationError(
                "This tag already exists.")
        return name

    def save(self, commit=True):
        tag = super().save(commit=False)
        if not tag.slug:        # only on creation
            tag.slug = slugify(tag.name)
        if commit:
            tag.save()
        return tag
