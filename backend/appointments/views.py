from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import date, datetime
from .models import DoctorSchedule, Appointment
from .serializers import (
    DoctorScheduleSerializer, 
    DoctorScheduleCreateSerializer,
    DoctorScheduleUpdateSerializer,
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentUpdateSerializer,
    AppointmentCancelSerializer,
    AppointmentReminderSerializer
)
from users.models import Doctor, Patient

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

# ===== APPOINTMENT VIEWS =====
@api_view(['POST'])
@permission_classes([AllowAny])
def create_appointment(request):
    """
    API đặt lịch khám cho bệnh nhân - tự động set reminder_enabled = False
    """
    serializer = AppointmentCreateSerializer(data=request.data)
    if serializer.is_valid():
        appointment = serializer.save()
        response_data = AppointmentSerializer(appointment).data
        return Response({
            'success': True,
            'message': 'Đặt lịch khám thành công',
            'data': response_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_appointments(request):
    """
    API lấy danh sách lịch khám
    Có thể lọc theo patient_id, doctor_id, appointment_date, status, reminder_enabled
    """
    appointments = Appointment.objects.select_related('patient__user', 'doctor__user').all()
    
    # Lọc theo patient_id
    patient_id = request.GET.get('patient_id')
    if patient_id:
        appointments = appointments.filter(patient_id=patient_id)
    
    # Lọc theo doctor_id
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
    
    # Lọc theo ngày
    appointment_date = request.GET.get('appointment_date')
    if appointment_date:
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            appointments = appointments.filter(appointment_date=appointment_date)
        except ValueError:
            return Response({
                'success': False,
                'message': 'Định dạng ngày không hợp lệ. Sử dụng YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Lọc theo trạng thái
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Lọc theo nhắc nhở
    reminder_filter = request.GET.get('reminder_enabled')
    if reminder_filter is not None:
        reminder_enabled = reminder_filter.lower() == 'true'
        appointments = appointments.filter(reminder_enabled=reminder_enabled)
    
    # Sắp xếp
    appointments = appointments.order_by('-appointment_date', 'time_slot')
    
    serializer = AppointmentSerializer(appointments, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': appointments.count()
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_appointment(request, pk):
    """
    API lấy chi tiết lịch khám
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    serializer = AppointmentSerializer(appointment)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_appointment(request, pk):
    """
    API sửa lịch khám
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    serializer = AppointmentUpdateSerializer(
        appointment,
        data=request.data,
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        response_data = AppointmentSerializer(appointment).data
        return Response({
            'success': True,
            'message': 'Cập nhật lịch khám thành công',
            'data': response_data
        })
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def cancel_appointment(request, pk):
    """
    API hủy lịch khám - tự động tắt nhắc nhở
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    serializer = AppointmentCancelSerializer(instance=appointment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = AppointmentSerializer(appointment).data
        return Response({
            'success': True,
            'message': 'Hủy lịch khám thành công',
            'data': response_data
        })
    
    return Response({
        'success': False,
        'message': 'Không thể hủy lịch khám',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def toggle_appointment_reminder(request, pk):
    """
    API bật/tắt nhắc nhở cho lịch khám
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    
    serializer = AppointmentReminderSerializer(
        appointment,
        data=request.data,
        partial=True
    )
    
    if serializer.is_valid():
        serializer.save()
        response_data = AppointmentSerializer(appointment).data
        status_text = "Bật" if appointment.reminder_enabled else "Tắt"
        return Response({
            'success': True,
            'message': f'{status_text} nhắc nhở thành công',
            'data': response_data
        })
    
    return Response({
        'success': False,
        'message': 'Không thể thay đổi cài đặt nhắc nhở',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_time_slots(request):
    """
    API lấy khung giờ trống của bác sĩ trong ngày
    """
    doctor_id = request.GET.get('doctor_id')
    appointment_date = request.GET.get('date')
    
    if not doctor_id or not appointment_date:
        return Response({
            'success': False,
            'message': 'Vui lòng cung cấp doctor_id và date'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    except (Doctor.DoesNotExist, ValueError):
        return Response({
            'success': False,
            'message': 'Bác sĩ không tồn tại hoặc định dạng ngày không hợp lệ'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Kiểm tra bác sĩ có lịch làm việc không
    doctor_schedule = DoctorSchedule.objects.filter(
        doctor=doctor,
        work_date=appointment_date,
        status__in=[DoctorSchedule.Status.SCHEDULED, DoctorSchedule.Status.ACTIVE]
    ).first()
    
    if not doctor_schedule:
        return Response({
            'success': False,
            'message': f'Bác sĩ {doctor.user.full_name} không có lịch làm việc ngày {appointment_date}'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Lấy các khung giờ đã đặt
    booked_slots = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
        status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED]
    ).values_list('time_slot', flat=True)
    
    # Tất cả khung giờ có thể
    all_slots = [choice[0] for choice in Appointment.TimeSlot.choices]
    
    # Khung giờ trống
    available_slots = [
        {
            'time_slot': slot,
            'display': dict(Appointment.TimeSlot.choices)[slot]
        }
        for slot in all_slots if slot not in booked_slots
    ]
    
    return Response({
        'success': True,
        'doctor': doctor.user.full_name,
        'date': appointment_date,
        'doctor_schedule': {
            'start_time': doctor_schedule.start_time,
            'end_time': doctor_schedule.end_time
        },
        'available_slots': available_slots,
        'count': len(available_slots)
    })

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_appointment(request, pk):
    """
    API xóa lịch khám (chỉ admin)
    """
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return Response({
        'success': True,
        'message': 'Xóa lịch khám thành công'
    }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_doctor_week_schedules(request, doctor_id):
    """
    API lấy lịch trình tuần của bác sĩ theo ID
    URL: /doctor/{doctor_id}/week/
    """
    try:
        doctor = Doctor.objects.select_related('user').get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response({
            'success': False,
            'message': f'Bác sĩ với ID {doctor_id} không tồn tại'
        }, status=status.HTTP_404_NOT_FOUND)
    
    from datetime import timedelta
    
    # Lấy tuần hiện tại hoặc tuần theo tham số
    week_date = request.GET.get('week_date')
    if week_date:
        try:
            base_date = datetime.strptime(week_date, '%Y-%m-%d').date()
        except ValueError:
            base_date = date.today()
    else:
        base_date = date.today()
    
    # Tính ngày đầu tuần (Thứ 2) và cuối tuần (Chủ nhật)
    start_of_week = base_date - timedelta(days=base_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Lấy tất cả lịch trình trong tuần
    schedules = DoctorSchedule.objects.filter(
        doctor=doctor,
        work_date__gte=start_of_week,
        work_date__lte=end_of_week
    ).order_by('work_date', 'start_time')
    
    serializer = DoctorScheduleSerializer(schedules, many=True)
    
    return Response({
        'success': True,
        'doctor_id': doctor.id,
        'doctor_name': doctor.user.full_name,
        'week_range': f"{start_of_week} đến {end_of_week}",
        'schedules': serializer.data,
        'count': schedules.count()
    })