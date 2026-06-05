

from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def home(request):

    if request.method == "POST":
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        if title:
            Task.objects.create(user=request.user,title=title, due_date=due_date if due_date else None,priority=priority)

    search = request.GET.get('search')
    filter_type = request.GET.get('filter')
    sort = request.GET.get('sort')

    tasks = Task.objects.filter(user=request.user)

    if search:
        tasks = tasks.filter(title__icontains=search)

    if filter_type == "completed":
        tasks = tasks.filter(completed=True)

    elif filter_type == "pending":
        tasks = tasks.filter(completed=False)
    if sort == "new":
        tasks = tasks.order_by('-id')

    elif sort == "old":
        tasks = tasks.order_by('id')

    elif sort == "high":
        tasks = tasks.order_by('priority')
        

    total_tasks = Task.objects.filter(user=request.user).count()

    completed_tasks = Task.objects.filter(
    user=request.user,
    completed=True
    ).count()
    pending_tasks = Task.objects.filter(
    user=request.user,
    completed=False
    ).count()
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress': progress,
}

    return render(request, 'home.html', context)


def delete_task(request, id):
    task = Task.objects.get(
    id=id,
    user=request.user
)
    task.delete()
    return redirect('/')
def complete_task(request, id):
    task = Task.objects.get(
    id=id,
    user=request.user
)

    task.completed = not task.completed
    task.save()

    return redirect('/')
def edit_task(request, id):

    task = Task.objects.get(
    id=id,
    user=request.user
)

    if request.method == "POST":
        title = request.POST.get('title')

        if title:
            task.title = title
            task.save()

        return redirect('/')

    return render(request, 'edit.html', {'task': task})