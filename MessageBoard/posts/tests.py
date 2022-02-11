from django.test import TestCase
from django.urls import reverse
from .models import Post
class PostModelTest(TestCase):
    def setUp(self):    # Automatically called by django
        Post.objects.create(text = "Just a test")
        
    def test_text_context(self): #Add test_ as prefix so django calls it automatically
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.text}'
        
        self.assertEqual(expected_object_name, 'Just a test')
        
class HomePageTest(TestCase):
    
    def setUp(self):
        Post.objects.create(text = "another test")
        
    def test_home_route(self):
        response = self.client.get(reverse('home'))     # reverse is equivalent of {{ url '' }} as in templates
        self.assertEqual(200, response.status_code)
        
    def test_template_used(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'home.html')