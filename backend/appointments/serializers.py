from rest_framework import serializers
from .models import DoctorSchedule
from users.models import Doctor
from users.serializers import UserSerializer

class DoctorScheduleSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    working_hours = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    
    class Meta:
        model = DoctorSchedule
        fields = [
            'id', 'doctor', 'doctor_name', 'doctor_specialization',
            'work_date', 'start_time', 'end_time', 'status', 'notes',
            'working_hours', 'is_today', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        """Validate dữ liệu đầu vào"""
        work_date = attrs.get('work_date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        doctor = attrs.get('doctor')
        
        # Kiểm tra thời gian hợp lệ
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("Giờ bắt đầu phải nhỏ hơn giờ kết thúc")
        
        # Kiểm tra không trùng lịch (nếu đang tạo mới)
        if not self.instance:  # Chỉ check khi tạo mới
            existing_schedule = DoctorSchedule.objects.filter(
                doctor=doctor,
                work_date=work_date
            ).exists()
            
            if existing_schedule:
                raise serializers.ValidationError(
                    f"Bác sĩ {doctor.user.full_name} đã có lịch trong ngày {work_date}"
                )
        
        return attrs

class DoctorScheduleCreateSerializer(serializers.ModelSerializer):
    """Serializer riêng cho việc tạo lịch - có thể nhập doctor_id"""
    
    class Meta:
        model = DoctorSchedule
        fields = ['doctor', 'work_date', 'start_time', 'end_time', 'status', 'notes']
    
    def validate_doctor(self, value):
        """Kiểm tra doctor tồn tại"""
        if not Doctor.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Bác sĩ không tồn tại")
        return value

class DoctorScheduleUpdateSerializer(serializers.ModelSerializer):
    """Serializer cho việc cập nhật lịch"""
    
    class Meta:
        model = DoctorSchedule
        fields = ['work_date', 'start_time', 'end_time', 'status', 'notes']
    
    def validate(self, attrs):
        work_date = attrs.get('work_date', self.instance.work_date)
        start_time = attrs.get('start_time', self.instance.start_time)
        end_time = attrs.get('end_time', self.instance.end_time)
        
        if start_time >= end_time:
            raise serializers.ValidationError("Giờ bắt đầu phải nhỏ hơn giờ kết thúc")
        
        return attrs