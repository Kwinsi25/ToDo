from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('add/', views.add_task, name='add-task'),
    path('edit/<int:pk>/', views.task_update, name='edit-task'),
    path('delete/<int:pk>/', views.delete_task, name='delete-task'),
    path('upcoming/', views.upcoming_tasks, name='upcoming-tasks'),
    path('today/', views.today_tasks, name='today-tasks'),
    path('personal/', views.personal_tasks, name='personal-tasks'),
    path('work/', views.work_tasks, name='work-tasks'),
]