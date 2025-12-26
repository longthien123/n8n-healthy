from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/n8n/', include('n8n.urls')),
    path('api/feedback/', include('feedback.urls')),  # THÊM MỚI: Feedback APIs
]
