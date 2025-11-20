from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import date, datetime
from .models import DoctorSchedule
from .serializers import (
    DoctorScheduleSerializer, 
    DoctorScheduleCreateSerializer,
    DoctorScheduleUpdateSerializer
)
from users.models import Doctor

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def create_doctor_schedule(request):
    """
    API tạo lịch trình cho bác sĩ
    """
    serializer = DoctorScheduleCreateSerializer(data=request.data)
    if serializer.is_valid():
        schedule = serializer.save()
        response_data = DoctorScheduleSerializer(schedule).data
        return Response({
            'success': True,
            'message': 'Tạo lịch trình thành công',
            'data': response_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_doctor_schedules(request):
    """
    API lấy danh sách lịch trình bác sĩ
    Có thể lọc theo doctor_id, work_date, status
    """
    schedules = DoctorSchedule.objects.select_related('doctor__user').all()
    
    # Lọc theo doctor_id
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        schedules = schedules.filter(doctor_id=doctor_id)
    
    # Lọc theo ngày
    work_date = request.GET.get('work_date')
    if work_date:
        try:
            work_date = datetime.strptime(work_date, '%Y-%m-%d').date()
            schedules = schedules.filter(work_date=work_date)
        except ValueError:
            return Response({
                'success': False,
                'message': 'Định dạng ngày không hợp lệ. Sử dụng YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Lọc theo trạng thái
    status_filter = request.GET.get('status')
    if status_filter:
        schedules = schedules.filter(status=status_filter)
    
    # Sắp xếp
    schedules = schedules.order_by('-work_date', 'start_time')
    
    serializer = DoctorScheduleSerializer(schedules, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': schedules.count()
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctor_schedule(request, pk):
    """
    API lấy chi tiết lịch trình bác sĩ
    """
    schedule = get_object_or_404(DoctorSchedule, pk=pk)
    serializer = DoctorScheduleSerializer(schedule)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_doctor_schedule(request, pk):
    """
    API cập nhật lịch trình bác sĩ
    """
    schedule = get_object_or_404(DoctorSchedule, pk=pk)
    
    # Kiểm tra quyền: chỉ admin hoặc chính bác sĩ đó mới được sửa
    if not (request.user.is_admin or 
            (request.user.is_doctor and request.user.doctor_profile == schedule.doctor)):
        return Response({
            'success': False,
            'message': 'Bạn không có quyền sửa lịch trình này'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = DoctorScheduleUpdateSerializer(
        schedule, 
        data=request.data, 
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        response_data = DoctorScheduleSerializer(schedule).data
        return Response({
            'success': True,
            'message': 'Cập nhật lịch trình thành công',
            'data': response_data
        })
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_doctor_schedule(request, pk):
    """
    API xóa lịch trình bác sĩ
    """
    schedule = get_object_or_404(DoctorSchedule, pk=pk)
    
    # Chỉ admin mới được xóa lịch trình
    # if not request.user.is_admin:
    #     return Response({
    #         'success': False,
    #         'message': 'Chỉ admin mới có quyền xóa lịch trình'
    #     }, status=status.HTTP_403_FORBIDDEN)
    
    schedule.delete()
    return Response({
        'success': True,
        'message': 'Xóa lịch trình thành công'
    }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctor_today_schedule(request, doctor_id):
    """
    API lấy lịch trình hôm nay của bác sĩ
    """
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    today = date.today()
    
    try:
        schedule = DoctorSchedule.objects.get(doctor=doctor, work_date=today)
        serializer = DoctorScheduleSerializer(schedule)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except DoctorSchedule.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Bác sĩ {doctor.user.full_name} không có lịch trình hôm nay'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_doctors_by_date(request):
    """
    API lấy danh sách bác sĩ có lịch trong ngày cụ thể
    """
    work_date = request.GET.get('date')
    if not work_date:
        return Response({
            'success': False,
            'message': 'Vui lòng cung cấp tham số date (YYYY-MM-DD)'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        work_date = datetime.strptime(work_date, '%Y-%m-%d').date()
    except ValueError:
        return Response({
            'success': False,
            'message': 'Định dạng ngày không hợp lệ. Sử dụng YYYY-MM-DD'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    schedules = DoctorSchedule.objects.filter(
        work_date=work_date,
        status__in=[DoctorSchedule.Status.SCHEDULED, DoctorSchedule.Status.ACTIVE]
    ).select_related('doctor__user')
    
    serializer = DoctorScheduleSerializer(schedules, many=True)
    return Response({
        'success': True,
        'date': work_date,
        'data': serializer.data,
        'count': schedules.count()
    })
