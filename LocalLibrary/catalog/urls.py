from django.urls import path
import catalog.views as views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('books', views.BookListView.as_view(), name = 'book_list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('authors', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail')
]
