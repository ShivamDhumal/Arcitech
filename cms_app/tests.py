from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import CustomUser, content_item

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'pincode': '123456',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserLoginLogoutTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'pincode': '123456',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }

        # Register a test user
        self.client.post(self.register_url, self.user_data, format='json')

    def test_user_login(self):
        login_data = {
            'username': 'testuser@example.com',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_logout(self):
        # Log the user in first
        login_data = {
            'username': 'testuser@example.com',
            'password': 'TestPass123!'
        }
        self.client.post(self.login_url, login_data, format='json')

        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ContentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'pincode': '123456',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }

        # Register a test user
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.content_data = {
            'user': self.user.id,
            'title': 'Test Content',
            'description': 'This is a test content.',
        }

    def test_create_content(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('content'), self.content_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_content(self):
        content = content_item.objects.create(**self.content_data)
        response = self.client.get(reverse('content-detail', kwargs={'id': content.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
