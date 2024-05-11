from django.http import HttpRequest
from django.shortcuts import redirect, render

from .models import Project
from .forms import ProjectForm


def projects(request: HttpRequest):
    """
    This function renders all the projects.
    """
    return render(
        request,
        "projects/projects.html",
        {"projects": Project.objects.all()},
    )


def project(request: HttpRequest, project_id: str):
    """
    This function is used to render the project page.
    """
    return render(
        request,
        "projects/project.html",
        {"project": Project.objects.get(id=project_id)},
    )


def create_project(request: HttpRequest):
    """
    This function is used to render the create project page.
    """
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context=context)


def update_project(request: HttpRequest, project_id: str):
    """
    This function is used to render the update project page.
    """
    project = Project.objects.get(id=project_id)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context=context)


def delete_project(request: HttpRequest, project_id: str):
    """
    This function is used to delete a project.
    """
    object = Project.objects.get(id=project_id)
    context = {"object": object}

    if request.method == "POST":
        object.delete()
        return redirect("projects")

    return render(request, "projects/delete_template.html", context)
