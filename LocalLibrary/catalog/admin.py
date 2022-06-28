from django.contrib import admin
from .models import Language, Genre, Book, BookInstance, Author

# Register your models here.

admin.site.register(Language)
admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)


class BookInline(admin.TabularInline):
    model = Book
    verbose_name = 'Book from Author'
    verbose_name_plural = "Books from Author"
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    fields = ('name', ('date_of_birth', 'date_of_death'))
    inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    verbose_name = "Book instance for the book"
    verbose_name_plural = "Book instances for the book"
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]
    

class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'id', 'due_back', 'borrower')
    
    fieldsets = (
        (None, {
            'fields': ('id', 'book', 'imprint')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
