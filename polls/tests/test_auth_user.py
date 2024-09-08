from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase


class AuthUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login(self):
        # login with test user
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)

        # check if user gets redirected
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

