from django.urls import path
from . import views

urlpatterns = [
    # Feedback Tasks endpoints
    path('tasks/', views.list_feedback_tasks, name='list_feedback_tasks'),
    path('tasks/create/', views.create_feedback_task, name='create_feedback_task'),
    path('tasks/<int:pk>/', views.get_feedback_task, name='get_feedback_task'),
    path('tasks/<int:pk>/update-status/', views.update_task_status, name='update_task_status'),
    path('tasks/<int:pk>/delete/', views.delete_feedback_task, name='delete_feedback_task'),
]
