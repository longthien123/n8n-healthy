from django.urls import path
from . import views

urlpatterns = [
    # Doctor Schedule endpoints
    path('schedules/', views.list_doctor_schedules, name='list_doctor_schedules'),
    path('schedules/create/', views.create_doctor_schedule, name='create_doctor_schedule'),
    path('schedules/<int:pk>/', views.get_doctor_schedule, name='get_doctor_schedule'),
    path('schedules/<int:pk>/update/', views.update_doctor_schedule, name='update_doctor_schedule'),
    path('schedules/<int:pk>/delete/', views.delete_doctor_schedule, name='delete_doctor_schedule'),
    path('schedules/<int:doctor_id>/week/', views.get_doctor_week_schedules, name='get_doctor_week_schedules'),
    
    # Special schedule endpoints
    path('schedules/doctor/<int:doctor_id>/today/', views.get_doctor_today_schedule, name='get_doctor_today_schedule'),
    path('schedules/available/', views.get_available_doctors_by_date, name='get_available_doctors_by_date'),
    
    # Appointment endpoints
    path('appointments/', views.list_appointments, name='list_appointments'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/<int:pk>/', views.get_appointment, name='get_appointment'),
    path('appointments/<int:pk>/update/', views.update_appointment, name='update_appointment'),
    path('appointments/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('appointments/<int:pk>/reminder/', views.toggle_appointment_reminder, name='toggle_appointment_reminder'),
    path('appointments/<int:doctor_id>/week/', views.get_doctor_week_schedules, name='get_doctor_week_schedules'),
    path('appointments/<int:appointment_id>/cancel-by-id/', views.cancel_appointment_by_id, name='cancel_appointment_by_id'),
    # Special appointment endpoints
    path('appointments/available-slots/', views.get_available_time_slots, name='get_available_time_slots'),
    
    # Doctor Dashboard endpoints (THÊM MỚI)
    path('appointments/doctor/<int:doctor_id>/', views.get_doctor_appointments, name='get_doctor_appointments'),
    path('appointments/<int:pk>/detail/', views.get_appointment_detail, name='get_appointment_detail'),
    path('appointments/<int:pk>/complete/', views.complete_appointment, name='complete_appointment'),
]