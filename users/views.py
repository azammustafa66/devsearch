import uuid
from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm


def profiles(request: HttpRequest):
    """
    This function returns all the profiles in the database
    """
    queryset = Profile.objects.all()
    context = {"profiles": queryset}
    return render(request, "users/profiles.html", context)


def profile(request: HttpRequest, id: uuid.uuid4):
    """
    This function returns a single profile based on the id
    """
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


@login_required(login_url="login")
def user_account(request: HttpRequest):
    """
    This function returns the user account page
    """
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
    }
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request: HttpRequest):
    """
    This function returns the edit account page
    """
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("account")

    context = {"profile": profile, "form": form}
    return render(request, "users/profile_form.html", context)


def login_user(request: HttpRequest):
    """
    This function logs in a user if the user exists in the database and the password is correct
    """
    # Redirect the user to the profiles page if they are already logged in
    if request.user.is_authenticated:
        return redirect("profiles")

    # Check if the user exists in the database and the password is correct
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "users/auth.html", {"page": "login"})


def logout_user(request: HttpRequest):
    """
    This function logs out a user from the application
    """
    logout(request)
    messages.info(request, "You are now logged out")
    return redirect("login")


def register_user(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("profiles")

    page = "register"
    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        try:
            user.username = username
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user)

            # Log in the user BEFORE redirecting
            login(request, user)
            messages.success(request, "User account was created successfully")
            return redirect("edit-account")

        except IntegrityError:
            messages.error(request, "A user with that username already exists.")
    else:
        for field in form:
            for error in field.errors:
                messages.error(request, f"{field.label}: {error}")

    context = {"page": page, "form": form}
    return render(request, "users/auth.html", context)
