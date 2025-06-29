from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError
from rest_framework.test import APIClient

from .models import Task
from .serializers import TaskSerializer


class TestTask(TestCase):
    def setUp(self):
        # Create a sample task for testing
        self.task = Task.objects.create(
            title="Test Task", description="This is a test task", completed=False
        )

    def test_task_read(self):
        """Test that a task can be read correctly"""
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertFalse(task.completed)

    def test_task_creation(self):
        """Test that a task can be created correctly"""
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertFalse(task.completed)

    def test_task_update(self):
        """Test that a task can be updated"""
        self.task.title = "Updated Task"
        self.task.completed = True
        self.task.save()

        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertTrue(updated_task.completed)

    def test_task_deletion(self):
        """Test that a task can be deleted"""
        task_id = self.task.id
        self.task.delete()

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

    def test_task_string_representation(self):
        """Test the string representation of a task"""
        self.assertEqual(str(self.task), self.task.title)

    def test_task_filtering(self):
        """Test filtering tasks"""
        Task.objects.create(
            title="Another Task", description="This is another task", completed=True
        )

        completed_tasks = Task.objects.filter(completed=True)
        incomplete_tasks = Task.objects.filter(completed=False)

        self.assertEqual(completed_tasks.count(), 1)
        self.assertEqual(incomplete_tasks.count(), 1)


class TestTaskSerializer(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task", description="This is a test task", completed=False
        )
        self.serializer = TaskSerializer(instance=self.task)

    def test_task_serializer_fields(self):
        """Test that the serializer returns the correct fields"""
        data = self.serializer.data
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "This is a test task")
        self.assertFalse(data["completed"])

    def test_task_serializer_validation(self):
        """Test that the serializer validates required fields"""
        serializer = TaskSerializer(data={"description": "No title"})
        self.assertFalse(serializer.is_valid())
        with self.assertRaises(ValidationError):
            serializer.validate(data={"description": "No title"})


class TestTaskAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user for authentication
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        # Force authenticate the client with the test user
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        """Clean up after tests"""
        self.client.force_authenticate(user=None)
        return super().tearDown()

    def test_task_api_create(self):
        """Test the API endpoint for creating a task"""
        response = self.client.post(
            "/tasks/",
            {
                "title": "API Task",
                "description": "This is a task created via API",
                "completed": False,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "API Task")
        self.assertEqual(response.data["description"], "This is a task created via API")
        self.assertFalse(response.data["completed"])

    def test_task_api_list(self):
        """Test the API endpoint for listing tasks"""
        Task.objects.create(
            title="API Task 1", description="First task via API", completed=False
        )
        Task.objects.create(
            title="API Task 2", description="Second task via API", completed=True
        )

        response = self.client.get("/tasks/", format="json")
        # print(response.data["results"][0]["title"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "API Task 1")

    def test_task_api_update(self):
        """Test the API endpoint for updating a task"""
        task = Task.objects.create(
            title="Task to Update",
            description="This task will be updated",
            completed=False,
        )

        response = self.client.put(
            f"/tasks/{task.id}/",
            {
                "title": "Updated Task",
                "description": "This task has been updated",
                "completed": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Updated Task")
        self.assertTrue(response.data["completed"])

    def test_task_api_delete(self):
        """Test the API endpoint for deleting a task"""
        task = Task.objects.create(
            title="Task to Delete",
            description="This task will be deleted",
            completed=False,
        )

        response = self.client.delete(f"/tasks/{task.id}/", format="json")

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task.id)

    def test_task_api_not_found(self):
        """Test the API endpoint for handling not found tasks"""
        response = self.client.get("/tasks/999/", format="json")
        # Assuming 999 is a non-existent task ID
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["detail"], "No Task matches the given query.")

    def test_task_api_validation_error(self):
        """Test the API endpoint for handling validation errors"""
        response = self.client.post(
            "/tasks/",
            {
                "description": "This task has no title",
                "completed": False,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)
        self.assertIsInstance(response.data["title"][0], ErrorDetail)
        self.assertRaises(ValidationError)
        self.assertEqual(str(response.data["title"][0]), "This field is required.")
