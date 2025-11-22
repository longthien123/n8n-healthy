from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.send_booking_to_n8n, name="send_booking_to_n8n"),
]
