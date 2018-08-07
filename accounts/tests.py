from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


# Create your tests here.
class AccountsTest(APITestCase):
    def setUp(self):

        self.test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword',
        )

        # URL for creating an account
        self.create_url = reverse('user-create')
        pass

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """

        data = {
            'username':'foobar',
            'email':'foobar@example.com',
            'password': 'somepassword',
        }

        # making a request to itself internally
        response = self.client.post(self.create_url,data=data,format='json')

        # we want to make sure we have 2 users in the database
        self.assertEqual(User.objects.count(),2)

        # we want to make sure it's returning 201 status code
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # Additionally, we want to return the username and email upon successful creation
        self.assertEqual(response.data['username'], data['username'])
        #self.assertEqual(response.data['password'], data['password'])

        self.assertFalse('password' in response.data)



