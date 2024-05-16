import uuid
from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile
from .forms import (
    CustomUserCreationForm,
    ProfileForm,
    SkillForm,
    MessageForm,
    NonAuthenticatedMessageForm,
)
from .utils import search_profiles, paginate_profiles


def login_user(request: HttpRequest):
    """
    This function logs in a user if the user exists in the database and the password is correct
    """
    # Redirect the user to the profiles page if they are already logged in
    if request.user.is_authenticated:
        return redirect("profiles")

    # Check if the user exists in the database and the password is correct
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")
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
    """
    This function registers a new user in the application
    """
    if request.user.is_authenticated:
        return redirect("profiles")

    page = "register"
    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)

            messages.success(request, "User account was created successfully")
            return redirect("edit-account")
        except IntegrityError:
            messages.error(request, "A user with that username already exists.")
    else:
        context = {"page": page, "form": form}
        return render(request, "users/auth.html", context)

    context = {"page": page, "form": form}
    return render(request, "users/auth.html", context)


def profiles(request: HttpRequest):
    """
    This function returns all the profiles in the database
    """
    profiles = Profile.objects.all()
    skills = None
    query = request.GET.get("q")
    if query:
        profiles, skills, query = search_profiles(request, query)

    profiles, custom_range = paginate_profiles(request, profiles, 6)
    context = {
        "profiles": profiles,
        "query": query,
        "skills": skills,
        "custom_range": custom_range,
    }
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


@login_required(login_url="login")
def create_skill(request: HttpRequest):
    """
    This function creates a new skill for the user
    """
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill created successfully")
            return redirect("account")

    context = {"profile": profile, "form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request: HttpRequest, id: uuid.uuid4):
    """
    This function creates a new skill for the user
    """
    profile = request.user.profile
    skill = profile.skill_set.get(id=str(id))
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill created successfully")
            return redirect("account")

    context = {"profile": profile, "form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request: HttpRequest, id: uuid.uuid4):
    """
    This function deletes a skill from the user's profile
    """
    profile = request.user.profile
    skill = profile.skill_set.get(id=str(id))
    context = {"object": skill}

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully")
        return redirect("account")

    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request: HttpRequest):
    """
    This function returns all the messages in the database
    """
    profile = request.user.profile
    messages_request = profile.messages.all()
    unread_count = profile.messages.filter(is_read=False).count()
    context = {"messages": messages_request, "unread_count": unread_count}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def view_message(request: HttpRequest, id: uuid.uuid4):
    """
    This function returns a single message based on the id
    """
    profile = request.user.profile
    message = profile.messages.get(id=str(id))
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def create_message(request: HttpRequest, recipient_id: uuid.UUID):
    """
    View function for creating a new message.
    Args:
        request (HttpRequest): The HTTP request object.
        recipient_id (uuid.UUID): The UUID of the recipient's profile.
    """
    recipient_profile = get_object_or_404(Profile, id=recipient_id)
    form = None

    if request.method == "POST":
        if not request.user.is_authenticated:
            form = NonAuthenticatedMessageForm(request.POST)
        else:
            form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.sender = request.user.profile
                message.name = request.user.profile.name
            else:
                message.name = form.cleaned_data["name"]
                message.email = form.cleaned_data["email"]

            message.recipient = recipient_profile
            message.save()
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
    else:
        if not request.user.is_authenticated:
            form = NonAuthenticatedMessageForm()
        else:
            form = MessageForm()

    context = {"form": form}
    return render(request, "users/message_form.html", context)
