# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from datetime import datetime, timedelta

def upcoming_tasks(request):
    tomorrow = timezone.now().date() + timedelta(days=1)  # Tomorrow's date
    tomorrow_tasks = Task.objects.filter(reminder_time__date__gte=tomorrow, completed=False).order_by('reminder_time')

    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow, completed=False).count()
    # Calculate today's tasks count
    today = timezone.now().date()
    today_count = Task.objects.filter(reminder_time__date=today, completed=False).count()

    # Filter personal tasks
    personal_tasks = Task.objects.filter(task_type='personal', completed=False).order_by('reminder_time')
    personal_count = personal_tasks.count()

     # Filter work tasks
    work_tasks = Task.objects.filter(task_type='work', completed=False).order_by('reminder_time')
    work_count = work_tasks.count()

    return render(request, 'tasks/upcoming_tasks.html', {'tasks': tomorrow_tasks,'upcoming_count': upcoming_count,'today_count': today_count,'personal_count':personal_count,'work_count':work_count})

def today_tasks(request):
    today = timezone.now().date()  # Today's date
    today_tasks = Task.objects.filter(reminder_time__date=today, completed=False).order_by('reminder_time')

    today_count = Task.objects.filter(reminder_time__date=today, completed=False).count()
    
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow, completed=False).count()

    # Filter personal tasks
    personal_tasks = Task.objects.filter(task_type='personal', completed=False).order_by('reminder_time')
    personal_count = personal_tasks.count()

    # Filter work tasks
    work_tasks = Task.objects.filter(task_type='work', completed=False).order_by('reminder_time')
    work_count = work_tasks.count()
    
    return render(request, 'tasks/today_tasks.html', {'tasks': today_tasks,'upcoming_count': upcoming_count,'today_count': today_count,'personal_count':personal_count,'work_count':work_count})


def personal_tasks(request):
    tomorrow = timezone.now().date() + timedelta(days=1)  # Tomorrow's date
    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow, completed=False).count()
    # Calculate today's tasks count
    today = timezone.now().date()
    today_count = Task.objects.filter(reminder_time__date=today, completed=False).count()

    # Filter personal tasks
    personal_tasks = Task.objects.filter(task_type='personal', completed=False).order_by('reminder_time')
    personal_count = personal_tasks.count()

    # Filter work tasks
    work_tasks = Task.objects.filter(task_type='work', completed=False).order_by('reminder_time')
    work_count = work_tasks.count()
    
    return render(request, 'tasks/personal_tasks.html', {
        'upcoming_count': upcoming_count,
        'today_count': today_count,
        'personal_tasks': personal_tasks,
        'personal_count': personal_count,
        'work_count':work_count

    })

def work_tasks(request):
    tomorrow = timezone.now().date() + timedelta(days=1)  # Tomorrow's date
    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow, completed=False).count()
    # Calculate today's tasks count
    today = timezone.now().date()
    today_count = Task.objects.filter(reminder_time__date=today, completed=False).count()

    # Filter personal tasks
    personal_tasks = Task.objects.filter(task_type='personal', completed=False).order_by('reminder_time')
    personal_count = personal_tasks.count()

    # Filter work tasks
    work_tasks = Task.objects.filter(task_type='work', completed=False).order_by('reminder_time')
    work_count = work_tasks.count()
    
    return render(request, 'tasks/work_tasks.html', {
        'upcoming_count': upcoming_count,
        'today_count': today_count,
        'personal_count': personal_count,
        'work_tasks': work_tasks,
        'work_count':work_count

    })


def task_list(request):
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow, completed=False).count()

    # Calculate today's tasks count
    today = timezone.now().date()
    today_count = Task.objects.filter(reminder_time__date=today, completed=False).count()

    # Filter personal tasks
    personal_tasks = Task.objects.filter(task_type='personal', completed=False).order_by('reminder_time')
    personal_count = personal_tasks.count()


    # Filter work tasks
    work_tasks = Task.objects.filter(task_type='work', completed=False).order_by('reminder_time')
    work_count = work_tasks.count()

    if request.method == 'POST':
        # Calculate upcoming tasks count (tomorrow and onward)
        
        date_filter = request.POST.get('date', None)
        if date_filter:
            try:
                date_filter = timezone.datetime.strptime(date_filter, '%Y-%m-%d').date()
                tasks = Task.objects.filter(reminder_time__date=date_filter).order_by('reminder_time')
            except ValueError:
                tasks = Task.objects.none()  # Handle invalid date format gracefully
        else:
            tasks = Task.objects.none()  # Handle no date filter provided
    else:
        tasks = Task.objects.filter(reminder_time__isnull=False, completed=False).order_by('reminder_time')
    
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'upcoming_count': upcoming_count,
        'today_count': today_count,
        'personal_count':personal_count,
        'work_count':work_count
    })

def add_task(request):
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow).count()

    # Calculate today's tasks count
    today = timezone.now().date()
    today_count = Task.objects.filter(reminder_time__date=today).count()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Task "{task.title}" added successfully.')
            return redirect('task-list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form,'upcoming_count': upcoming_count,
        'today_count': today_count,})

def task_update(request, pk):
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow).count()

    # Calculate today's tasks count
    today = timezone.now().date()
    today_count = Task.objects.filter(reminder_time__date=today).count()
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if task.completed:
                task.reminder_time = None
                task.is_reminder_set = False
            task.save()
            messages.success(request, f'Task "{task.title}" updated successfully.')
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form,'upcoming_count': upcoming_count,
        'today_count': today_count,})

def delete_task(request, pk):
    tomorrow = timezone.now().date() + timedelta(days=1)
    upcoming_count = Task.objects.filter(reminder_time__date__gte=tomorrow).count()

    # Calculate today's tasks count
    today = timezone.now().date()
    today_count = Task.objects.filter(reminder_time__date=today).count()
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        confirm = request.POST.get('confirm_delete', False)
        if confirm:
            task.delete()
            messages.success(request, f'Task "{task.title}" deleted successfully.')
            return redirect('task-list')
        else:
            messages.info(request, 'Deletion canceled.')
            return redirect('task-list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task,'upcoming_count': upcoming_count,
        'today_count': today_count,})
