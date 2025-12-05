from django.urls import path
from .views import HomeView, TaskDetailView, TaskCreateView, TaskDeleteView
app_name = 'todo'   #reverse با namespace

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),   # use <pk>
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
