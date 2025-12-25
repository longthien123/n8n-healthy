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


class Doctor(models.Model):
    """
    Thông tin chi tiết của Bác sĩ
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, verbose_name="Chuyên khoa")
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Số chứng chỉ hành nghề")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Số năm kinh nghiệm")
    bio = models.TextField(blank=True, verbose_name="Giới thiệu")
    
    class Meta:
        db_table = 'doctors'
        verbose_name = 'Bác sĩ'
        verbose_name_plural = 'Bác sĩ'
    
    def __str__(self):
        return f"BS. {self.user.full_name} - {self.specialization}"


class Patient(models.Model):
    """
    Thông tin chi tiết của Bệnh nhân
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_code = models.CharField(max_length=20, unique=True, verbose_name="Mã bệnh nhân")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    gender = models.CharField(
        max_length=10,
        choices=[('MALE', 'Nam'), ('FEMALE', 'Nữ'), ('OTHER', 'Khác')],
        default='OTHER',
        verbose_name="Giới tính"
    )
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    emergency_contact = models.CharField(max_length=15, blank=True, verbose_name="Liên hệ khẩn cấp")
    blood_type = models.CharField(max_length=5, blank=True, verbose_name="Nhóm máu")
    allergies = models.TextField(blank=True, verbose_name="Dị ứng")
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Bệnh nhân'
        verbose_name_plural = 'Bệnh nhân'
    
    def __str__(self):
        return f"{self.patient_code} - {self.user.full_name}"
