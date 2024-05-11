import uuid
from django.shortcuts import render

from .models import Profile


def profiles(request):
    queryset = Profile.objects.all()
    context = {"profiles": queryset}
    return render(request, "users/profiles.html", context=context)


def profile(request, id: uuid.UUID):
    queryset = Profile.objects.get(id=str(id))
    top_skills = queryset.skill_set.exclude(description__exact="")
    other_skills = queryset.skill_set.filter(description="")
    projects = queryset.project_set.all()
    context = {
        "profile": queryset,
        "top_skills": top_skills,
        "other_skills": other_skills,
        "projects": projects,
    }
    return render(request, "users/profile.html", context)
