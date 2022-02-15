from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy, reverse

# Create your views here.

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    
class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    
class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = '__all__'
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'body']
    
    '''
    Use success url in UpdateView instead of get_absolute_url as UpdateView calls success_url instead.
    '''
    def get_success_url(self) -> str:
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
