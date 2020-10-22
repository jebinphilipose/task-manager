import csv
import logging
from celery import shared_task
from celery.signals import worker_shutting_down
from django.db import IntegrityError
from .models import Task, User


@shared_task
def delete_task(result, task_id):
    task = Task.objects.get(id=task_id)
    if (task.status != Task.TaskStatus.COMPLETED):
        task.delete()
    return


@worker_shutting_down.connect
def worker_shutting_down_handler(sig, how, exitcode, **kwargs):
    print('Deleting uncompleted tasks')
    Task.objects.exclude(status=Task.TaskStatus.COMPLETED).delete()


@shared_task
def import_csv_data(csv_file_path, task_id):
    try:
        # Update Task status to PROCESSING
        task = Task.objects.get(id=task_id)
        task.status = Task.TaskStatus.PROCESSING
        task.save()

        # Reading CSV file
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip CSV column headers
            next(csv_reader)

            for row in csv_reader:
                # Fetch latest Task details
                task = Task.objects.get(id=task_id)

                if task.status == Task.TaskStatus.PAUSED:
                    print(f'Task with id: {task.id} is {task.status}')

                # Pause execution if status is PAUSED
                while task.status == Task.TaskStatus.PAUSED:
                    # Fetch latest Task details
                    task = Task.objects.get(id=task_id)

                # Delete records if status is CANCELLED
                if task.status == Task.TaskStatus.CANCELLED:
                    print(f'Task with id: {task.id} is {task.status}')
                    return task.status

                elif task.status == Task.TaskStatus.PROCESSING:
                    print(f'Task with id: {task.id} is {task.status}')
                    try:
                        # add row to database
                        user = User.objects.create(task_id=task,
                                                username=row[0],
                                                name=row[1],
                                                email=row[2],
                                                sex=row[3],
                                                birthdate=row[4],
                                                is_active=row[5],
                                                date_joined=row[6])
                    except IntegrityError:
                        pass

    except BaseException:
        if Task.objects.filter(id=task_id).first():
            # Log the exception with stack trace
            logging.exception('Fatal error occured')
            # Update Task status to FAILED
            task.status = Task.TaskStatus.FAILED
            task.save()
        return Task.TaskStatus.FAILED

    # Update Task status to COMPLETED
    task.status = Task.TaskStatus.COMPLETED
    task.save()

    return task.status
