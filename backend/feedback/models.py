from django.db import models


class ClinicFeedbackTask(models.Model):
    """
    Model quản lý feedback từ khách hàng về phòng khám
    Dữ liệu từ Google Form sẽ được n8n gửi vào bảng này
    """
    
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Chờ xử lý'
        FINISHED = 'Finished', 'Đã hoàn thành'
    
    # Thông tin khách hàng
    customer_email = models.EmailField(max_length=255)
    
    # Các điểm đánh giá
    score_doctor_attitude = models.CharField(max_length=50, blank=True, null=True)  # Tệ/Bình Thường/Tốt
    score_doctor_clarity = models.CharField(max_length=50, blank=True, null=True)  # Không/Có
    score_waiting_time = models.CharField(max_length=50, blank=True, null=True)  # Lâu/Bình Thường/Nhanh
    score_procedure_speed = models.CharField(max_length=50, blank=True, null=True)  # Không/Bình Thường/Nhanh
    score_cleanliness = models.CharField(max_length=50, blank=True, null=True)  # Có/Không
    score_staff_attitude = models.CharField(max_length=50, blank=True, null=True)  # Tệ/Bình Thường/Tốt
    
    # Góp ý từ khách hàng
    customer_comment = models.TextField(blank=True, null=True)
    
    # Trạng thái xử lý
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clinic_feedback_tasks'
        ordering = ['-created_at']
        verbose_name = 'Feedback Task'
        verbose_name_plural = 'Feedback Tasks'
    
    def __str__(self):
        return f"Feedback from {self.customer_email} - {self.status}"
    
    @property
    def has_negative_feedback(self):
        """Kiểm tra có feedback tiêu cực không"""
        negative_keywords = ['Tệ', 'Không', 'Lâu']
        scores = [
            self.score_doctor_attitude,
            self.score_doctor_clarity,
            self.score_waiting_time,
            self.score_procedure_speed,
            self.score_cleanliness,
            self.score_staff_attitude,
        ]
        return any(score in negative_keywords for score in scores if score)
