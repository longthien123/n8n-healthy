from django.urls import path
from . import views

urlpatterns = [
    # Doctor Schedule endpoints
    path('schedules/', views.list_doctor_schedules, name='list_doctor_schedules'),
    path('schedules/create/', views.create_doctor_schedule, name='create_doctor_schedule'),
    path('schedules/<int:pk>/', views.get_doctor_schedule, name='get_doctor_schedule'),
    path('schedules/<int:pk>/update/', views.update_doctor_schedule, name='update_doctor_schedule'),
    path('schedules/<int:pk>/delete/', views.delete_doctor_schedule, name='delete_doctor_schedule'),
    
    # Special endpoints
    path('schedules/doctor/<int:doctor_id>/today/', views.get_doctor_today_schedule, name='get_doctor_today_schedule'),
    path('schedules/available/', views.get_available_doctors_by_date, name='get_available_doctors_by_date'),
]