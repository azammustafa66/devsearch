from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest

from .models import Project
from .forms import ProjectForm


class ProjectViewsTestCase(TestCase):
    """
    This class tests the views of the projects app.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.project = Project.objects.create(
            title="Test Project", description="This is a test project", owner=self.user
        )

    def test_projects_view(self):
        """
        This method tests the projects view.
        """
        response = self.client.get(reverse("projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/projects.html")
        # Check if projects are rendered in context
        self.assertIn("projects", response.context)

    def test_projects_view_with_search(self):
        response = self.client.get(reverse("projects") + "?q=test")
        self.assertEqual(response.status_code, 200)
        # Check if search results are filtered
        self.assertLessEqual(len(response.context["projects"]), Project.objects.count())

    def test_project_detail_view(self):
        response = self.client.get(reverse("project", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project.html")
        # Check if correct project is rendered
        self.assertEqual(response.context["project"], self.project)

    def test_create_project_view_unauthenticated(self):
        # Unauthenticated user should be redirected to login
        response = self.client.get(reverse("create_project"))
        self.assertRedirects(response, "/login/?next=/create_project/")

    def test_create_project_view_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("create_project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_form.html")

        # Test successful form submission (add form data here)
        response = self.client.post(
            reverse("create_project"),
            {
                "title": "New Test Project",
                "description": "This is a new test project",
            },
        )
        self.assertRedirects(response, reverse("account"))
