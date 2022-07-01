from os import name
from django.urls import path
import catalog.views as views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('books', views.BookListView.as_view(), name = 'book_list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('authors', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('mybooks', views.LoanedBooksByUserListView.as_view(), name = 'loaned_books'),
    path('borrowed', views.LoanedBooksLibrarianListView.as_view(), name = 'loaned_books_librarian'),
    path('book/<uuid:pk>/renew', views.renew_book_librarian, name = 'renew_book_librarian'),
    path('author/create', views.AuthorCreateView.as_view(), name = 'author_create'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name = 'author_update'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name = 'author_delete'),
    path('book/create', views.BookCreateView.as_view(), name = 'book_create'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name = 'book_update'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name = 'book_delete'),
]
