from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class TaskLoginView(LoginView):
    template_name = 'Todoapp/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('list')
    
class TaskRegisterView(FormView):
    template_name = 'Todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(TaskRegisterView, self).form_valid(form)
        
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list')
        return super(TaskRegisterView, self).get(*args, **kwargs)
    

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        
        search_input = self.request.GET.get('search-area') or ''
        context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        return context
    
 
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ('title', 'description', 'complete')
    context_object_name = 'createtask'
    template_name = "Todoapp/create.html"
    success_url = reverse_lazy('list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ('title', 'description', 'complete')
    template_name = "Todoapp/update.html"
    success_url = reverse_lazy('list')
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "Todoapp/delete.html"
    success_url = reverse_lazy('list')


    
