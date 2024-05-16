from django.test import TestCase
from rest_framework.test import APIClient


class ProjectListTest(TestCase):
    def set_up(self):
        self.client = APIClient()

    def test_get_projects(self):
        response = self.client.get("/api/v1/projects/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
