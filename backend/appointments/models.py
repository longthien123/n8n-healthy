from django.db import models
from django.core.exceptions import ValidationError
from users.models import Doctor

class DoctorSchedule(models.Model):
    """
    Model lịch trình làm việc của bác sĩ
    """
    
    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Đã lên lịch'
        ACTIVE = 'ACTIVE', 'Đang làm việc'
        COMPLETED = 'COMPLETED', 'Hoàn thành'
        CANCELLED = 'CANCELLED', 'Đã hủy'
    
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='schedules',
        verbose_name="Bác sĩ"
    )
    
    work_date = models.DateField(
        verbose_name="Ngày làm việc"
    )
    
    start_time = models.TimeField(
        verbose_name="Giờ bắt đầu"
    )
    
    end_time = models.TimeField(
        verbose_name="Giờ kết thúc"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name="Trạng thái"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Ghi chú"
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
        db_table = 'doctor_schedules'
        verbose_name = 'Lịch trình bác sĩ'
        verbose_name_plural = 'Lịch trình bác sĩ'
        # Một bác sĩ chỉ có 1 lịch trình trong 1 ngày
        unique_together = ['doctor', 'work_date']
        ordering = ['-work_date', 'start_time']
    
    def __str__(self):
        return f"{self.doctor.user.full_name} - {self.work_date} ({self.start_time}-{self.end_time})"
    
    def clean(self):
        """Validate dữ liệu"""
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("Giờ bắt đầu phải nhỏ hơn giờ kết thúc")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def working_hours(self):
        """Tính số giờ làm việc trong ngày"""
        from datetime import datetime, timedelta
        start_dt = datetime.combine(self.work_date, self.start_time)
        end_dt = datetime.combine(self.work_date, self.end_time)
        delta = end_dt - start_dt
        return round(delta.total_seconds() / 3600, 2)  # Số giờ
    
    @property
    def is_today(self):
        """Kiểm tra có phải lịch hôm nay không"""
        from datetime import date
        return self.work_date == date.today()
