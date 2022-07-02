from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render

from .forms import CustomUserCreationForm
# Create your views here.

def home(request):
    context = {'test': 'THISISTESTCONTEXT'}
    return render(request, template_name='home.html', context=context)
    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    

