from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Project, Tag


def search_projects(request, query: str):
    """
    This function is used to search for projects
    """
    if request.GET.get("q"):
        query = request.GET.get("q")

    tags = Tag.objects.filter(name__icontains=query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(owner__name__icontains=query)
        | Q(tags__in=tags)
    )

    return projects, query


def paginate_projects(request, projects, results_per_page):
    """
    This function is used to paginate projects
    """
    page = request.GET.get("page")
    paginator = Paginator(projects, results_per_page)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = int(page) - 4
    if left_index <= 1:
        left_index = 1

    right_index = int(page) + 5
    if right_index >= paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return projects, custom_range, paginator
