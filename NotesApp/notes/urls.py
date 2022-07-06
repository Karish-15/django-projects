from django.urls import path
from notes import views

urlpatterns = [
    path('create', views.create_note, name='create'),
    path('<uuid:id>', views.detail_note, name='note_detail'),
    path('<uuid:id>/edit', views.edit_note, name='note_edit'),
    path('<uuid:id>/delete', views.delete_note, name='note_delete')
]
