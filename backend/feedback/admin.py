from django.contrib import admin
from .models import ClinicFeedbackTask


@admin.register(ClinicFeedbackTask)
class ClinicFeedbackTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_email', 'status', 'has_negative_feedback', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_email', 'customer_comment']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin khách hàng', {
            'fields': ('customer_email',)
        }),
        ('Đánh giá', {
            'fields': (
                'score_doctor_attitude',
                'score_doctor_clarity',
                'score_waiting_time',
                'score_procedure_speed',
                'score_cleanliness',
                'score_staff_attitude',
            )
        }),
        ('Góp ý', {
            'fields': ('customer_comment',)
        }),
        ('Trạng thái', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
