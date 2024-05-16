from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Profile, Skill


def search_profiles(request, query: str):
    """
    This function is used to search for profiles that match the query.
    """
    if request.GET.get("q"):
        query = request.GET.get("q")

    skills = Skill.objects.filter(name__icontains=query)

    if query:
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=query) | Q(intro__icontains=query) | Q(skill__in=skills)
        )

    return profiles, skills, query


def paginate_profiles(request, profiles, results_per_page):
    """
    This function is used to paginate profiles
    """
    page = request.GET.get("page", 1)
    paginator = Paginator(profiles, results_per_page)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return profiles, custom_range
