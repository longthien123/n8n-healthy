from django.db import models
from django.core.exceptions import ValidationError
from users.models import Doctor, Patient

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


class Appointment(models.Model):
    """
    Model lịch khám bệnh - Đơn giản với các trường cơ bản
    """
    
    class Status(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Đã đặt lịch'
        CONFIRMED = 'CONFIRMED', 'Đã xác nhận'
        COMPLETED = 'COMPLETED', 'Hoàn thành'
        CANCELLED = 'CANCELLED', 'Đã hủy'
        NO_SHOW = 'NO_SHOW', 'Không đến'
    
    class TimeSlot(models.TextChoices):
        # Buổi sáng
        SLOT_08_00 = '08:00-09:00', '08:00 - 09:00'
        SLOT_09_00 = '09:00-10:00', '09:00 - 10:00'
        SLOT_10_00 = '10:00-11:00', '10:00 - 11:00'
        SLOT_11_00 = '11:00-12:00', '11:00 - 12:00'
        # Buổi chiều
        SLOT_14_00 = '14:00-15:00', '14:00 - 15:00'
        SLOT_15_00 = '15:00-16:00', '15:00 - 16:00'
        SLOT_16_00 = '16:00-17:00', '16:00 - 17:00'
        SLOT_17_00 = '17:00-18:00', '17:00 - 18:00'
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Bệnh nhân"
    )
    
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Bác sĩ"
    )
    
    appointment_date = models.DateField(
        verbose_name="Ngày khám"
    )
    
    time_slot = models.CharField(
        max_length=20,
        choices=TimeSlot.choices,
        verbose_name="Khung giờ khám (1 tiếng)"
    )
    
    reminder_enabled = models.BooleanField(
        default=False,
        verbose_name="Bật nhắc nhở"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name="Trạng thái"
    )
    
    reason = models.TextField(
        blank=True,
        verbose_name="Lý do khám"
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
        db_table = 'appointments'
        verbose_name = 'Lịch khám'
        verbose_name_plural = 'Lịch khám'
        # Một bác sĩ không thể có 2 lịch khám cùng ngày và giờ
        unique_together = ['doctor', 'appointment_date', 'time_slot']
        ordering = ['-appointment_date', 'time_slot']
    
    def __str__(self):
        return f"{self.patient.user.full_name} - BS.{self.doctor.user.full_name} - {self.appointment_date} {self.time_slot}"
    
    def clean(self):
        """Validate dữ liệu"""
        # Kiểm tra bác sĩ có lịch làm việc trong ngày đó không
        if not DoctorSchedule.objects.filter(
            doctor=self.doctor,
            work_date=self.appointment_date,
            status__in=[DoctorSchedule.Status.SCHEDULED, DoctorSchedule.Status.ACTIVE]
        ).exists():
            raise ValidationError(f"Bác sĩ {self.doctor.user.full_name} không có lịch làm việc ngày {self.appointment_date}")
        
        # Kiểm tra trùng lịch khám
        if self.pk is None:  # Chỉ check khi tạo mới
            if Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                time_slot=self.time_slot,
                status__in=[self.Status.SCHEDULED, self.Status.CONFIRMED]
            ).exists():
                raise ValidationError(f"Khung giờ {self.time_slot} ngày {self.appointment_date} đã có người đặt")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def can_cancel(self):
        """Kiểm tra có thể hủy lịch không"""
        from datetime import date, datetime, timedelta
        
        # Chỉ có thể hủy nếu trạng thái là SCHEDULED hoặc CONFIRMED
        if self.status not in [self.Status.SCHEDULED, self.Status.CONFIRMED]:
            return False
        
        # Chỉ có thể hủy trước 24h
        return self.appointment_date > date.today()
    
    @property
    def is_today(self):
        """Kiểm tra có phải lịch hôm nay không"""
        from datetime import date
        return self.appointment_date == date.today()
