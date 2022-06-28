from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_authors = Author.objects.all().count()
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }
    
    return render(request, 'index.html', context=context)

class BookListView(ListView):
    model = Book
    # Either this template in 'templates' folder or in 'templates/catalog/ModelName_list.html
    # template_name = 'book_list.html'
    
    context_object_name = 'book_list'
    paginate_by = 8
class BookDetailView(DetailView):
    model = Book
    
    contex_object_name = 'book'
    
class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'    
    
class AuthorListView(ListView):
    model = Author
    context_object_name = 'author_list'
    paginate_by = 12
    
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    paginate_by = 10
    template_name='catalog/bookinstance_list_borrowed_user.html'
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

