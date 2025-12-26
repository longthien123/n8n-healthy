from rest_framework import serializers
from .models import ClinicFeedbackTask


class FeedbackTaskSerializer(serializers.ModelSerializer):
    """Serializer cho Feedback Task - hiển thị đầy đủ thông tin"""
    has_negative_feedback = serializers.ReadOnlyField()
    
    class Meta:
        model = ClinicFeedbackTask
        fields = [
            'id', 'customer_email',
            'score_doctor_attitude', 'score_doctor_clarity',
            'score_waiting_time', 'score_procedure_speed',
            'score_cleanliness', 'score_staff_attitude',
            'customer_comment', 'status', 'has_negative_feedback',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FeedbackTaskCreateSerializer(serializers.ModelSerializer):
    """Serializer cho việc tạo feedback từ n8n webhook"""
    
    class Meta:
        model = ClinicFeedbackTask
        fields = [
            'customer_email',
            'score_doctor_attitude', 'score_doctor_clarity',
            'score_waiting_time', 'score_procedure_speed',
            'score_cleanliness', 'score_staff_attitude',
            'customer_comment'
        ]


class FeedbackTaskUpdateStatusSerializer(serializers.ModelSerializer):
    """Serializer cho việc cập nhật trạng thái (Pending -> Finished)"""
    
    class Meta:
        model = ClinicFeedbackTask
        fields = ['status']
    
    def validate_status(self, value):
        """Chỉ cho phép chuyển sang Finished"""
        if value not in [ClinicFeedbackTask.Status.PENDING, ClinicFeedbackTask.Status.FINISHED]:
            raise serializers.ValidationError("Trạng thái không hợp lệ")
        return value
