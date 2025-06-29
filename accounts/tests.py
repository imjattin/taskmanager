from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import UserLoginSerializer, UserRegisterSerializer

User = get_user_model()


class UserViewsTestCase(APITestCase):
    """
    Test cases for user authentication views (UserRegisterView and UserLoginView).
    """

    def setUp(self):
        # Create a test user for login tests
        self.login_url = "/accounts/login/"
        self.register_url = "/accounts/register/"
        self.refresh_url = "/accounts/refresh/"
        self.verify_url = "/accounts/verify/"

        self.test_user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="existingpass123",
        )

    def test_user_registration_success(self):
        """Test successful user registration."""
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Check if user was created
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_regsitration_invalid_data(self):
        """Test user registration with invalid data."""
        response = self.client.post(
            self.register_url,
            {
                "username": "",  # Empty username
                "email": "invalid-email",  # Invalid email format
                "password": "123",  # Too short password
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_user_login_success(self):
        """Test successful user login."""
        login_data = {"username": "existinguser", "password": "existingpass123"}
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials."""
        login_data = {"username": "existinguser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_missing_data(self):
        """Test user login with missing data."""
        login_data = {
            "username": "existinguser"
            # Missing password
        }
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_refresh(self):
        """Test token refresh functionality."""
        # First, get tokens by logging in
        login_data = {"username": "existinguser", "password": "existingpass123"}
        login_response = self.client.post(self.login_url, login_data, format="json")
        refresh_token = login_response.data["refresh"]

        # Now test refresh
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_verify(self):
        """Test token verification functionality."""
        # Get access token
        login_data = {"username": "existinguser", "password": "existingpass123"}
        login_response = self.client.post(self.login_url, login_data, format="json")
        access_token = login_response.data["access"]

        # Verify token
        verify_data = {"token": access_token}
        response = self.client.post(self.verify_url, verify_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserSerializersTestCase(TestCase):
    """
    Test cases for user serializers (UserRegisterSerializer and UserLoginSerializer).
    """

    def setUp(self):
        """Set up test data."""
        self.valid_register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }

        self.invalid_register_data = {
            "username": "",
            "email": "invalid-email",
            "password": "123",  # Too short
        }

        # Create a test user for login serializer tests
        self.test_user = User.objects.create_user(
            username="loginuser", email="login@example.com", password="loginpass123"
        )

    def test_user_register_serializer_valid_data(self):
        """Test UserRegisterSerializer with valid data."""
        serializer = UserRegisterSerializer(data=self.valid_register_data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_register_serializer_invalid_data(self):
        """Test UserRegisterSerializer with invalid data."""
        serializer = UserRegisterSerializer(data=self.invalid_register_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_user_register_serializer_missing_required_fields(self):
        """Test UserRegisterSerializer with missing required fields."""
        incomplete_data = {"username": "testuser"}
        serializer = UserRegisterSerializer(data=incomplete_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_user_register_serializer_password_write_only(self):
        """Test that password field is write-only in UserRegisterSerializer."""
        serializer = UserRegisterSerializer(data=self.valid_register_data)
        serializer.is_valid()
        user = serializer.save()

        # Create a new serializer instance for the created user
        user_serializer = UserRegisterSerializer(user)

        # Password should not be in the serialized data
        self.assertNotIn("password", user_serializer.data)

    def test_user_register_serializer_duplicate_username(self):
        """Test UserRegisterSerializer with duplicate username."""
        # Create first user
        User.objects.create_user(
            username="duplicateuser", email="first@example.com", password="firstpass123"
        )

        # Try to create another user with same username
        duplicate_data = {
            "username": "duplicateuser",
            "email": "second@example.com",
            "password": "secondpass123",
        }
        serializer = UserRegisterSerializer(data=duplicate_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_user_login_serializer_valid_credentials(self):
        """Test UserLoginSerializer with valid credentials."""
        login_data = {"username": "loginuser", "password": "loginpass123"}
        serializer = UserLoginSerializer(data=login_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.test_user)

    def test_user_login_serializer_invalid_credentials(self):
        """Test UserLoginSerializer with invalid credentials."""
        login_data = {"username": "loginuser", "password": "wrongpassword"}
        serializer = UserLoginSerializer(data=login_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_user_login_serializer_nonexistent_user(self):
        """Test UserLoginSerializer with non-existent user."""
        login_data = {"username": "nonexistentuser", "password": "somepassword"}
        serializer = UserLoginSerializer(data=login_data)

        self.assertFalse(serializer.is_valid())
