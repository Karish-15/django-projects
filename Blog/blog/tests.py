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
        
    def test_get_absolute_url(self):
        url = self.post.get_absolute_url()
        self.assertEqual('/post/1', url)
        
    def test_post_create_view(self):
        resp = self.client.post(reverse('post_new'), {
        'title': 'New title',
        'body': 'New text',
        'author': self.user,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'New title')
        
    def test_post_update_view(self):
        resp = self.client.post(reverse('post_update', args=[1]), {
            'title': 'Updated title',
            'body': 'Updated body',
        })
        self.assertEqual(resp.status_code, 302)
        
        # Check if post was actually updated
        resp = self.client.get(reverse('post_detail', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Updated title')        
        
    def test_post_delete_view(self):
        resp = self.client.post(reverse('post_delete', args=[1]))
        
        self.assertEqual(302, resp.status_code)
        self.assertEqual(list(Post.objects.all()), [])
        
        
        