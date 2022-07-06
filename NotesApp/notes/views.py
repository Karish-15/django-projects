from django.shortcuts import render, HttpResponseRedirect
from django.template import context
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Notes
from .forms import NoteCreateForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        notes_list = Notes.objects.filter(author = request.user).all().order_by('last_edit')
        context = {
            'notes_list': notes_list
        }
        
        return render(request, template_name='home_auth.html', context = context)
    
    return render(request, template_name='home_unauth.html')

@login_required
def create_note(request):
    form = NoteCreateForm(request.POST)
    
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return HttpResponseRedirect(reverse('index'))
        
    context = {
        'form': form,
    }
    return render(request, template_name='note_create.html', context = context)

@login_required
def detail_note(request, id):
    note = Notes.objects.filter(id = id)[0]
    
    context = {
        'note': note,
    }
    return render(request, template_name='note_detail.html', context=context)

@login_required
def edit_note(request, id):
    note = Notes.objects.filter(id=id)[0]
    if request.method == 'POST':
        form = NoteCreateForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('note_detail', kwargs={'id': id}))
    
    form = NoteCreateForm(instance=note)
    context = {
        'form': form,
    }
    return render(request, template_name='note_edit.html', context=context)

@login_required
def delete_note(request, id):
    if request.method == 'POST':
        note = Notes.objects.filter(id=id)[0]
        note.delete()
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, template_name='note_delete.html')