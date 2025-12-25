from rest_framework import serializers
from .models import DoctorSchedule, Appointment
from users.models import Doctor, Patient
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

# ===== APPOINTMENT SERIALIZERS =====
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.full_name', read_only=True)
    patient_code = serializers.CharField(source='patient.patient_code', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    can_cancel = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'patient_code',
            'doctor', 'doctor_name', 'doctor_specialization',
            'appointment_date', 'time_slot', 'reminder_enabled', 'status', 
            'reason', 'notes', 'can_cancel', 'is_today', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Serializer cho việc đặt lịch khám - tự động set reminder_enabled = False"""
    
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'time_slot', 'reason', 'notes']
    
    def create(self, validated_data):
        # Tự động set reminder_enabled = False khi đặt lịch mới
        validated_data['reminder_enabled'] = False
        return super().create(validated_data)
    
    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        appointment_date = attrs.get('appointment_date')
        time_slot = attrs.get('time_slot')
        
        # Kiểm tra bác sĩ có lịch làm việc không
        if not DoctorSchedule.objects.filter(
            doctor=doctor,
            work_date=appointment_date,
            status__in=[DoctorSchedule.Status.SCHEDULED, DoctorSchedule.Status.ACTIVE]
        ).exists():
            raise serializers.ValidationError(
                f"Bác sĩ {doctor.user.full_name} không có lịch làm việc ngày {appointment_date}"
            )
        
        # Kiểm tra khung giờ đã có người đặt chưa
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=time_slot,
            status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED]
        ).exists():
            raise serializers.ValidationError(
                f"Khung giờ {time_slot} ngày {appointment_date} đã có người đặt"
            )
        
        # Kiểm tra bệnh nhân đã có lịch khám trong ngày chưa (optional)
        existing_appointment = Appointment.objects.filter(
            patient=patient,
            appointment_date=appointment_date,
            status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED]
        ).exists()
        
        if existing_appointment:
            raise serializers.ValidationError(
                f"Bệnh nhân đã có lịch khám trong ngày {appointment_date}"
            )
        
        return attrs
    
    def validate_patient(self, value):
        """Kiểm tra patient tồn tại"""
        if not Patient.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Bệnh nhân không tồn tại")
        return value
    
    def validate_doctor(self, value):
        """Kiểm tra doctor tồn tại"""
        if not Doctor.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Bác sĩ không tồn tại")
        return value

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer cho việc sửa lịch khám"""
    
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'time_slot', 'reminder_enabled', 'reason', 'notes', 'status']
    
    def validate(self, attrs):
        appointment_date = attrs.get('appointment_date', self.instance.appointment_date)
        time_slot = attrs.get('time_slot', self.instance.time_slot)
        
        # Kiểm tra trạng thái có thể sửa không
        if self.instance.status in [Appointment.Status.COMPLETED, Appointment.Status.CANCELLED]:
            raise serializers.ValidationError("Không thể sửa lịch khám đã hoàn thành hoặc đã hủy")
        
        # Nếu thay đổi ngày hoặc giờ, kiểm tra trùng lịch
        if (appointment_date != self.instance.appointment_date or 
            time_slot != self.instance.time_slot):
            
            # Kiểm tra bác sĩ có lịch làm việc không
            if not DoctorSchedule.objects.filter(
                doctor=self.instance.doctor,
                work_date=appointment_date,
                status__in=[DoctorSchedule.Status.SCHEDULED, DoctorSchedule.Status.ACTIVE]
            ).exists():
                raise serializers.ValidationError(
                    f"Bác sĩ {self.instance.doctor.user.full_name} không có lịch làm việc ngày {appointment_date}"
                )
            
            # Kiểm tra khung giờ mới có trùng không
            if Appointment.objects.filter(
                doctor=self.instance.doctor,
                appointment_date=appointment_date,
                time_slot=time_slot,
                status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED]
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    f"Khung giờ {time_slot} ngày {appointment_date} đã có người đặt"
                )
        
        return attrs

class AppointmentCancelSerializer(serializers.Serializer):
    """Serializer cho việc hủy lịch khám"""
    cancel_reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        if not self.instance.can_cancel:
            raise serializers.ValidationError("Không thể hủy lịch khám này")
        return attrs
    
    def save(self):
        cancel_reason = self.validated_data.get('cancel_reason', '')
        self.instance.status = Appointment.Status.CANCELLED
        # Tự động tắt nhắc nhở khi hủy lịch
        self.instance.reminder_enabled = False
        
        if cancel_reason:
            current_notes = self.instance.notes or ''
            self.instance.notes = f"Lý do hủy: {cancel_reason}\n{current_notes}".strip()
        
        self.instance.save()
        return self.instance

class AppointmentReminderSerializer(serializers.ModelSerializer):
    """Serializer riêng cho việc bật/tắt nhắc nhở"""
    
    class Meta:
        model = Appointment
        fields = ['reminder_enabled']
    
    def validate(self, attrs):
        # Chỉ có thể bật nhắc nhở cho lịch khám chưa hoàn thành/hủy
        if self.instance.status in [Appointment.Status.COMPLETED, Appointment.Status.CANCELLED]:
            raise serializers.ValidationError("Không thể bật nhắc nhở cho lịch khám đã hoàn thành hoặc đã hủy")
        return attrs


# ===== DOCTOR DASHBOARD SERIALIZERS (THÊM MỚI) =====
class PatientDetailSerializer(serializers.ModelSerializer):
    """Serializer trả về đầy đủ thông tin patient (dùng cho Doctor Dashboard)"""
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'patient_code', 'full_name', 'email', 'phone',
                  'date_of_birth', 'gender', 'blood_type', 'address', 
                  'allergies', 'emergency_contact']


class DoctorDetailSerializer(serializers.ModelSerializer):
    """Serializer trả về đầy đủ thông tin doctor (dùng cho Doctor Dashboard)"""
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'email', 'phone', 'specialization', 
                  'license_number', 'experience_years']


class AppointmentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer cho Doctor Dashboard - trả về đầy đủ thông tin patient và doctor
    Thay vì chỉ trả về patient_name, patient_code
    """
    patient = PatientDetailSerializer(read_only=True)
    doctor = DoctorDetailSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor',
            'appointment_date', 'time_slot', 'status', 
            'reason', 'notes', 'reminder_enabled',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']