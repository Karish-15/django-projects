from django.contrib import admin
from .models import Notes

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title','author' ,'date_created',)
    exclude = ('date_created', 'last_edit',)
    
admin.site.register(Notes, NoteAdmin)
