import os.path
import json
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .models import Task, User
from .tasks import import_csv_data, export_csv_data

# Create your views here.
@csrf_exempt
def pause_task(request, task_id):
    if request.method == 'PATCH':
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.PAUSED
        task.save()
        return JsonResponse({'response': f'Task with id: {task.id} paused'})
    else:
        raise Http404

@csrf_exempt
def resume_task(request, task_id):
    if request.method == 'PATCH':
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.PROCESSING
        task.save()
        return JsonResponse({'response': f'Task with id: {task.id} resumed'})
    else:
        raise Http404

@csrf_exempt
def cancel_task(request, task_id):
    if request.method == 'PATCH':
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.CANCELLED
        task.save()
        return JsonResponse({'response': f'Task with id: {task.id} cancelled'})
    else:
        raise Http404

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        # Create a new Task
        task = Task.objects.create(type='import_csv_data')
        # Run Celery task
        filename = os.path.dirname(os.path.dirname(__file__)) + '/users.csv'
        import_csv_data.delay(filename, task.id)
        return JsonResponse({'response': f'CSV upload with Task id: {task.id} started'}, status=201)
    else:
        raise Http404

@csrf_exempt
def download_csv(request):
    if request.method == 'POST':
        from_date = json.loads(request.body)['from_date']
        # Create a new Task
        task = Task.objects.create(type='export_csv_data')
        # Run Celery task
        filename = os.path.dirname(os.path.dirname(__file__)) + '/export.csv'
        export_csv_data.delay(filename, task.id, from_date)
        return JsonResponse({'response': f'CSV download with Task id: {task.id} started'})
    else:
        raise Http404
