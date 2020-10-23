import os.path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from .tasks import import_csv_data, delete_task

# Create your views here.
@csrf_exempt
def pause_task(request, task_id):
    if request.method == 'PATCH':
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.PAUSED
        task.save()
        return JsonResponse({'response': f'Task with id: {task.id} paused'})

@csrf_exempt
def resume_task(request, task_id):
    if request.method == 'PATCH':
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.PROCESSING
        task.save()
        return JsonResponse({'response': f'Task with id: {task.id} resumed'})

@csrf_exempt
def cancel_task(request, task_id):
    if request.method == 'PATCH':
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.CANCELLED
        task.save()
        return JsonResponse({'response': f'Task with id: {task.id} cancelled'})

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        # Create a new Task
        task = Task.objects.create(type='import_csv_data')
        # Run Celery task
        import_csv_data.apply_async((os.path.dirname(os.path.dirname(__file__)) + '/users.csv', task.id), link=delete_task.s(task.id))
        return JsonResponse({'response': f'CSV upload with Task id: {task.id} started'}, status=201)
