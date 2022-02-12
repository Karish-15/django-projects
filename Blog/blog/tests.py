from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

from .models import Post

class BlogTest(TestCase):
    
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        
        self.post = Post.objects.create(
            title='good title',
            body='LALALALALALA',
            author = self.user
        )
        
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'LALALALALALA')
        
    def test_post_list_view(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(200, resp.status_code)
        self.assertContains(resp, 'LALALALALALA')
        self.assertTemplateUsed(resp, 'home.html')
        
    def test_post_detail_view(self):
        resp = self.client.get('/post/1')
        no_response = self.client.get('/post/23')
        
        self.assertEqual(200, resp.status_code)
        self.assertEqual(404, no_response.status_code)
        self.assertContains(resp, 'good title')
        self.assertTemplateUsed(resp, 'post_detail.html')
