from django.urls import path
from . import views

urlpatterns = [
    # User endpoints
    path('create/', views.create_user, name='create_user'),
    path('list/', views.list_users, name='list_users'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('me/', views.current_user, name='current_user'),
    
    # Admin endpoint
    path('admin/create/', views.create_admin, name='create_admin'),
    
    # Doctor endpoints
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('doctors/create/', views.create_doctor, name='create_doctor'),
    path('doctors/<int:pk>/', views.get_doctor, name='get_doctor'),
    path('doctors/<int:pk>/update/', views.update_doctor, name='update_doctor'),
    path('doctors/<int:pk>/delete/', views.delete_doctor, name='delete_doctor'),
    
    # Patient endpoints
    path('patients/', views.list_patients, name='list_patients'),
    path('patients/create/', views.create_patient, name='create_patient'),
    path('patients/<int:pk>/', views.get_patient, name='get_patient'),
    path('patients/<int:pk>/update/', views.update_patient, name='update_patient'),
    path('patients/<int:pk>/delete/', views.delete_patient, name='delete_patient'),
    path('patient/user/<int:user_id>/', views.get_patient_by_user_id, name='get_patient_by_user_id'),
    path('create_patient/', views.create_patient, name='create_patient'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),

    # 2. [QUAN TRỌNG] Các đường dẫn đặc biệt (Thêm mới vào đây)
    # Phải đặt TRÊN dòng <int:pk> để không bị lỗi
    path('patients/me/', views.get_my_patient_profile, name='my_patient_profile'),
    path('patients/by-user/<int:user_id>/', views.get_patient_by_user_id, name='get_patient_by_user_id'),

    # 3. Các đường dẫn tìm theo ID Bệnh nhân (Đặt dưới cùng)
    path('patients/<int:pk>/', views.get_patient, name='get_patient'),
    path('patients/<int:pk>/update/', views.update_patient, name='update_patient'),
    path('patients/<int:pk>/delete/', views.delete_patient, name='delete_patient'),
]