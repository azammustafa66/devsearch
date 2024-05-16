from django.forms import ModelForm
from django import forms

from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "demo_link",
            "source_link",
            "featured_image",
            "tags",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["vote_type", "body"]
        labels = {
            "value": "Place your vote",
            "body": "Add a comment with your vote",
        }
        widgets = {
            "value": forms.Select(attrs={"class": "select"}),
            "body": forms.Textarea(attrs={"class": "textarea"}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
