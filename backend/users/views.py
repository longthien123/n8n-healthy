from django.shortcuts import render, get_object_or_404
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

# ===== PATIENT VIEWS =====
@api_view(['POST'])
@permission_classes([AllowAny])
def create_patient(request):
    """API tạo bệnh nhân mới"""
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        return Response({
            'success': True,
            'message': 'Tạo bệnh nhân thành công',
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