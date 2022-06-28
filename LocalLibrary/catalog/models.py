from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

import uuid

# Create your models here.

class Language(models.Model):
    lang = models.CharField(max_length=100, help_text="Enter the language the book is written in")
    
    def __str__(self):
        return self.lang
    
    
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Entre a book genre")
    
    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    lang = models.ForeignKey(Language, help_text="Select the language the book is available in", on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})
    
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    
    display_genre.short_description = 'Genre'
    
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, help_text="Unique ID for book instance (Automatically generated)", default=uuid.uuid4)
    due_back = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, null=True, on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )
    
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank = True, default='m', help_text='Book Availability')
    
    class Meta:
        ordering = ['due_back']
        
    def __str__(self) -> str:
        return f'{self.id} ({self.book.title})'
    
    def is_overdue(self):
        return bool(self.due_back and date.today()>self.due_back)
    
    
class Author(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        permissions = (
            ('can_mark_returned', 'Set book as returned'),
        )
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})
    
    

    