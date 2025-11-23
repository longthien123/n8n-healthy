from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.send_booking_to_n8n, name="send_booking_to_n8n"),
    path('cron-check/', views.trigger_reminders_view, name='trigger_reminders'),
]
