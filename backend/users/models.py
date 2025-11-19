from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Model User tùy chỉnh cho hệ thống quản lý sức khỏe
    """
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Quản trị viên'
        DOCTOR = 'DOCTOR', 'Bác sĩ' 
        PATIENT = 'PATIENT', 'Bệnh nhân'
    
    # Các trường bắt buộc
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.PATIENT,
        verbose_name="Vai trò"
    )
    
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name="Số điện thoại"
    )
    
    full_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Họ và tên"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang hoạt động"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'

    def __str__(self):
        return f"{self.full_name or self.username} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_doctor(self):
        return self.role == self.Role.DOCTOR
    
    @property
    def is_patient(self):
        return self.role == self.Role.PATIENT
