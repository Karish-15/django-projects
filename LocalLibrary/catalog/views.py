from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book, BookInstance, Author
from .forms import RenewBookModelForm

import datetime

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

@login_required()
@user_passes_test(lambda u: u.has_perm('catalog.can_mark_returned'))
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk = pk)
    
    if request.method == 'POST':
        
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            
            return HttpResponseRedirect(reverse('loaned_books_librarian'))
    else:
        proposed_renewal = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal})
    
    ## For when GET request or form is not valid.
    context = {
            'form': form,
            'book_instance': book_instance, 
        }
        
    return render(request, template_name= 'catalog/book_renew_librarian.html', context=context)


# CBVs

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
    
class LoanedBooksLibrarianListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ['catalog.can_mark_returned']
    
    model = BookInstance
    template_name = 'catalog/bookinstance_list_librarian.html'
    
    def get_queryset(self):
        return BookInstance.objects.filter(status = 'o').order_by('due_back')
    

# Generic CBVs
#Author
class AuthorCreateView(CreateView, PermissionRequiredMixin):
    permission_required = ['catalog.can_mark_returned']
    model = Author
    fields = ['name', 'date_of_birth', 'date_of_death']
    
class AuthorUpdateView(UpdateView, PermissionRequiredMixin):
    permission_required = ['catalog.can_mark_returned']
    model = Author
    fields = '__all__'
    
class AuthorDeleteView(DeleteView, PermissionRequiredMixin):
    permission_required = ['catalog.can_mark_returned']
    model = Author
    success_url = reverse_lazy('author_list')
    
#Book
class BookCreateView(CreateView, PermissionRequiredMixin):
    permission_required = ['catalog.can_mark_returned']
    model = Book
    fields = ['title', 'author', 'summary', 'summary', 'isbn', 'genre', 'lang']
    
class BookUpdateView(UpdateView, PermissionRequiredMixin):
    permission_required = ['catalog.can_mark_returned']
    model = Book
    fields = ['title', 'author', 'summary', 'summary', 'isbn', 'genre', 'lang']
    
class BookDeleteView(DeleteView, PermissionRequiredMixin):
    permission_required = ['catalog.can_mark_returned']
    model = Book
    success_url = reverse_lazy('book_list')



