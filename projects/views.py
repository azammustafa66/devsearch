from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate_projects


def projects(request: HttpRequest):
    """
    This function renders all the projects or search results.
    """
    projects = Project.objects.all()
    query = request.GET.get("q")

    projects, custom_range, paginator = paginate_projects(request, projects, 6)

    if query:
        projects, query = search_projects(request, query)

    context = {
        "projects": projects,
        "query": query,
        "paginator": paginator,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


def project(request: HttpRequest, project_id: str):
    """
    This function is used to render the project page.
    """
    project = Project.objects.get(id=project_id)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            project = Project.objects.get(id=project_id)
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.get_vote_count
            messages.success(request, "Review was successfully added")
            return redirect("project", project_id=project.id)

    context = {"project": project, "form": form}
    return render(request, "projects/project.html", context)


@login_required(login_url="login")
def create_project(request: HttpRequest):
    """
    This function is used to render the create project page.
    """
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request: HttpRequest, project_id: str):
    """
    This function is used to render the update project page.
    """
    profile = request.user.profile
    project = profile.project_set.get(id=project_id)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request: HttpRequest, project_id: str):
    """
    This function is used to delete a project.
    """
    profile = request.user.profile
    object = profile.project_set.get(id=project_id)

    if request.method == "POST":
        object.delete()
        return redirect("account")

    context = {"object": object}
    return render(request, "delete_template.html", context)
