from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User, Doctor, Patient

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'full_name', 'phone', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Mật khẩu xác nhận không khớp")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        # create_user đã tự động hash password, không cần set_password lại
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'role', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        print(username, password, "validate")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Tên đăng nhập hoặc mật khẩu không đúng')
            if not user.is_active:
                raise serializers.ValidationError('Tài khoản đã bị khóa')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Phải nhập tên đăng nhập và mật khẩu')
        
        return attrs

# ===== ADMIN SERIALIZER =====
class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'full_name', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Mật khẩu xác nhận không khớp")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Tạo admin user
        user = User.objects.create_user(
            password=password,
            role=User.Role.ADMIN,
            **validated_data
        )
        
        # Cấp quyền superuser và staff
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        return user

# ===== DOCTOR SERIALIZERS =====
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    full_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'username', 'email', 'password', 'full_name', 'phone',
                  'specialization', 'license_number', 'experience_years', 'bio']
    
    def create(self, validated_data):
        # Tách thông tin user
        password = validated_data.pop('password')
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'full_name': validated_data.pop('full_name'),
            'phone': validated_data.pop('phone', ''),
            'role': User.Role.DOCTOR
        }
        
        # Tạo user (create_user đã tự động hash password)
        user = User.objects.create_user(password=password, **user_data)
        
        # Tạo doctor profile
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

class DoctorUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', required=False)
    phone = serializers.CharField(source='user.phone', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = Doctor
        fields = ['full_name', 'phone', 'email', 'specialization', 
                  'license_number', 'experience_years', 'bio']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        
        # Cập nhật user
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        
        # Cập nhật doctor
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

# ===== PATIENT SERIALIZERS =====
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    full_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Patient
        fields = ['id', 'user', 'username', 'email', 'password', 'full_name', 'phone',
                  'patient_code', 'date_of_birth', 'gender', 'address', 
                  'emergency_contact', 'blood_type', 'allergies']
    
    def create(self, validated_data):
        # Tách thông tin user
        password = validated_data.pop('password')
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'full_name': validated_data.pop('full_name'),
            'phone': validated_data.pop('phone', ''),
            'role': User.Role.PATIENT
        }
        
        # Tạo user (create_user đã tự động hash password)
        user = User.objects.create_user(password=password, **user_data)
        
        # Tạo patient profile
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

class PatientUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', required=False)
    phone = serializers.CharField(source='user.phone', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    
    class Meta:
        model = Patient
        fields = ['full_name', 'phone', 'email', 'patient_code', 'date_of_birth', 
                  'gender', 'address', 'emergency_contact', 'blood_type', 'allergies']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        
        # Cập nhật user
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        
        # Cập nhật patient
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance