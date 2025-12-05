from django.views.generic import DetailView, CreateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Task


class HomeView(ListView):
    model = Task
    template_name = 'home.html'  # Changed from 'todo/home.html'
    context_object_name = 'tasks'
    ordering = ['due_date', 'due_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        today = now.date()
        time_str = now.strftime('%H:%M:%S')

        context['overdue_tasks'] = Task.overdue_unfinished().order_by('due_date', 'due_time')
        
        # Active tasks: future dates or today with future/equal time
        context['active_tasks'] = Task.objects.filter(
            done=False
        ).extra(
            where=["(due_date > %s) OR (due_date = %s AND due_time >= %s)"],
            params=[today, today, time_str]
        ).order_by('due_date', 'due_time')
        
        context['completed_tasks'] = Task.objects.filter(done=True).order_by('due_date', 'due_time')
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'  # Changed from 'todo/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'due_time']
    template_name = 'task_create.html'  # Changed from 'todo/task_create.html'
    success_url = reverse_lazy('todo:home')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_delete.html'  # Changed from 'todo/task_delete.html'
    success_url = reverse_lazy('todo:home')
    context_object_name = 'task'