from django.shortcuts import render, get_object_or_404
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import (
    UserCreateSerializer, UserSerializer, LoginSerializer, AdminSerializer,
    DoctorSerializer, DoctorUpdateSerializer,
    PatientSerializer, PatientUpdateSerializer
)
from .models import User, Doctor, Patient
from django.views.decorators.csrf import csrf_exempt

# --- IMPORTS CHO VIỆC KÍCH HOẠT TÀI KHOẢN ---
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token # Import file vừa tạo ở Bước 1
from django.conf import settings # Để lấy domain nếu có cấu hình


# ===== USER VIEWS =====
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """API tạo người dùng mới"""
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response({
            'success': True,
            'message': 'Tạo người dùng thành công',
            'data': user_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_users(request):
    """API lấy danh sách người dùng"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """API đăng nhập"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user_data = UserSerializer(user).data
        return Response({
            'success': True,
            'message': 'Đăng nhập thành công',
            'data': {
                'user': user_data,
                'session_id': request.session.session_key
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Đăng nhập thất bại',
        'errors': serializer.errors
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_user(request):
    """API đăng xuất"""
    logout(request)
    return Response({
        'success': True,
        'message': 'Đăng xuất thành công'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    """API lấy thông tin user hiện tại"""
    serializer = UserSerializer(request.user)
    return Response({
        'success': True,
        'data': serializer.data
    })

# ===== DOCTOR VIEWS =====
@api_view(['POST'])
@permission_classes([AllowAny])
def create_doctor(request):
    """API tạo bác sĩ mới"""
    serializer = DoctorSerializer(data=request.data)
    if serializer.is_valid():
        doctor = serializer.save()
        return Response({
            'success': True,
            'message': 'Tạo bác sĩ thành công',
            'data': DoctorSerializer(doctor).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_doctors(request):
    """API lấy danh sách bác sĩ"""
    doctors = Doctor.objects.select_related('user').all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctor(request, pk):
    """API lấy thông tin chi tiết bác sĩ"""
    doctor = get_object_or_404(Doctor, pk=pk)
    serializer = DoctorSerializer(doctor)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_doctor(request, pk):
    """API cập nhật thông tin bác sĩ"""
    doctor = get_object_or_404(Doctor, pk=pk)
    serializer = DoctorUpdateSerializer(doctor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Cập nhật thành công',
            'data': DoctorSerializer(doctor).data
        })
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_doctor(request, pk):
    """API xóa bác sĩ"""
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    doctor.delete()
    user.delete()
    return Response({
        'success': True,
        'message': 'Xóa bác sĩ thành công'
    }, status=status.HTTP_204_NO_CONTENT)

# ===== ACTIVATION VIEW (Thêm mới) =====

@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    """API xử lý link kích hoạt từ Email"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Token hợp lệ -> Kích hoạt tài khoản
        user.is_active = True
        user.save()
        
        # Cách 1: Redirect thẳng về trang Login của React Frontend
        # return redirect('http://localhost:3000/login?status=activated')
        
        # Cách 2: Trả về JSON thông báo (Nếu muốn hiển thị giao diện từ backend hoặc test Postman)
        return Response({
            'success': True,
            'message': 'Kích hoạt tài khoản thành công! Bạn có thể đăng nhập ngay bây giờ.'
        }, status=status.HTTP_200_OK)
        
    else:
        return Response({
            'success': False,
            'message': 'Link kích hoạt không hợp lệ hoặc đã hết hạn.'
        }, status=status.HTTP_400_BAD_REQUEST)



# ===== PATIENT VIEWS =====
@api_view(['POST'])
@permission_classes([AllowAny])
def create_patient(request):
    """API tạo bệnh nhân mới với xác thực Email qua n8n"""
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        # 1. Lưu Patient và User (Lúc này user.is_active mặc định là True)
        patient = serializer.save()
        user = patient.user # Lấy user liên kết với bệnh nhân này
        
        # 2. Deactivate tài khoản ngay lập tức
        user.is_active = False
        user.save()

        # 3. Tạo Link kích hoạt
        # Mã hóa User ID và tạo Token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        
        # Tạo đường dẫn đầy đủ (Thay đổi domain localhost bằng domain thật khi deploy)
        # Ví dụ: http://127.0.0.1:8000/api/activate/MQ/bv2-321.../
        domain = "https://healthybackend.onrender.com" 
        activation_link = f"{domain}/api/users/activate/{uid}/{token}/"

        # 4. Gửi Webhook sang n8n
        # Đây là URL Webhook bạn lấy từ n8n Node
        n8n_webhook_url = "http://localhost:5678/webhook/send-activation-email" 
        
        payload = {
            "email": user.email,
            "full_name": f"{user.full_name}",
            "activation_link": activation_link
        }

        try:
            # Gửi request sang n8n (timeout 3s để không treo server nếu n8n chậm)
            requests.post(n8n_webhook_url, json=payload, timeout=3)
        except requests.exceptions.RequestException as e:
            print(f"Lỗi gửi webhook sang n8n: {e}")
            # Có thể log lỗi nhưng vẫn trả về thành công cho User biết để check mail
        
        return Response({
            'success': True,
            'message': 'Đăng ký thành công! Vui lòng kiểm tra email để kích hoạt tài khoản.',
            'data': PatientSerializer(patient).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_patients(request):
    """API lấy danh sách bệnh nhân"""
    patients = Patient.objects.select_related('user').all()
    serializer = PatientSerializer(patients, many=True)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_patient(request, pk):
    """API lấy thông tin chi tiết bệnh nhân"""
    patient = get_object_or_404(Patient, pk=pk)
    serializer = PatientSerializer(patient)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_patient(request, pk):
    """API cập nhật thông tin bệnh nhân"""
    patient = get_object_or_404(Patient, pk=pk)
    serializer = PatientUpdateSerializer(patient, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Cập nhật thành công',
            'data': PatientSerializer(patient).data
        })
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_patient(request, pk):
    """API xóa bệnh nhân"""
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    patient.delete()
    user.delete()
    return Response({
        'success': True,
        'message': 'Xóa bệnh nhân thành công'
    }, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])  # Có thể đổi thành AllowAny nếu chỉ admin mới tạo được admin
def create_admin(request):
    """
    API tạo admin mới
    """
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        user_data = UserSerializer(admin).data
        return Response({
            'success': True,
            'message': 'Tạo admin thành công',
            'data': user_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_patient_by_user_id(request, user_id):
    """
    API hiển thị patient theo ID user
    """
    try:
        user = User.objects.get(id=user_id)
        
        if not user.is_patient:
            return Response({
                'success': False,
                'message': f'User ID {user_id} không phải là bệnh nhân'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        patient = Patient.objects.select_related('user').get(user=user)
        serializer = PatientSerializer(patient)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
        
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': f'User với ID {user_id} không tồn tại'
        }, status=status.HTTP_404_NOT_FOUND)
    except Patient.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Không tìm thấy thông tin bệnh nhân cho User ID {user_id}'
        }, status=status.HTTP_404_NOT_FOUND)
    


# ===== MY PROFILE VIEWS =====

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Bắt buộc đăng nhập mới xem được
def get_my_patient_profile(request):
    """API lấy hồ sơ bệnh nhân của người đang đăng nhập"""
    user = request.user
    try:
        # Tìm hồ sơ bệnh nhân gắn với user này
        # Lưu ý: Nếu model Patient bạn để related_name khác thì sửa 'patient' thành tên đó
        # Thường mặc định Django nối ngược qua user.patient (nếu OneToOneField không set related_name)
        # Hoặc user.patient_set.first() nếu là ForeignKey
        
        # Cách an toàn nhất: Query trực tiếp bảng Patient
        patient = Patient.objects.get(user=user) 
        serializer = PatientSerializer(patient)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Patient.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Người dùng này chưa tạo hồ sơ bệnh nhân'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_patient_by_user_id(request, user_id):
    """
    API tìm hồ sơ bệnh nhân dựa theo user_id
    """
    try:
        # Tìm trong bảng Patient xem dòng nào có user_id trùng khớp
        patient = Patient.objects.get(user__id=user_id)
        serializer = PatientSerializer(patient)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Patient.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Không tìm thấy hồ sơ bệnh nhân nào gắn với User ID {user_id}'
        }, status=status.HTTP_404_NOT_FOUND)