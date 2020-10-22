import uuid
from django.db import models


class DateTimeWithoutTZField(models.DateTimeField):
    def db_type(self, connection):
        return 'timestamp'

# Create your models here.
class Task(models.Model):
    class TaskStatus(models.TextChoices):
        CREATED = 'CREATED'
        PROCESSING = 'PROCESSING'
        PAUSED = 'PAUSED'
        CANCELLED = 'CANCELLED'
        COMPLETED = 'COMPLETED'
        FAILED = 'FAILED'

    type = models.CharField(max_length=100)
    created_at = DateTimeWithoutTZField(auto_now_add=True)
    updated_at = DateTimeWithoutTZField(auto_now=True)
    status = models.CharField(max_length=10, choices=TaskStatus.choices, default=TaskStatus.CREATED)

    def __str__(self):
        return self.type



class User(models.Model):
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE, db_index=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    sex = models.CharField(max_length=1)
    birthdate = models.DateField()
    is_active = models.BooleanField()
    date_joined = DateTimeWithoutTZField()

    def __str__(self):
        return self.name
