from django.urls import path
from .views import upload_csv, pause_task, resume_task, cancel_task


urlpatterns = [
    path('task/<int:task_id>/pause/', pause_task, name="pause_task"),
    path('task/<int:task_id>/resume/', resume_task, name="resume_task"),
    path('task/<int:task_id>/cancel/', cancel_task, name="cancel_task"),
    path('upload/', upload_csv, name="upload_csv"),
]
