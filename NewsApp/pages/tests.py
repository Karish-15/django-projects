from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class HomePageTests(SimpleTestCase):
    
    def test_home_status(self):
        resp = self.client.get('/')
        self.assertEqual(200, resp.status_code)
        
    def test_home_status_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(200, resp.status_code)
        
    def test_home_template(self):
        resp = self.client.get(reverse('home'))
        self.assertTemplateUsed(resp, 'home.html')
        
        
class SignUpPageTests(TestCase):
    
    email = 'test@email.com'
    username = 'test_username'
    
    def test_signup_status(self):
        resp = self.client.get('/')
        self.assertEqual(200, resp.status_code)
        
    def test_signup_status_by_name(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(200, resp.status_code)
        
    def test_signup_template(self):
        resp = self.client.get(reverse('signup'))
        self.assertTemplateUsed(resp, 'signup.html')
        
    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)