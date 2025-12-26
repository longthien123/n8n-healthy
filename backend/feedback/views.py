from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ClinicFeedbackTask
from .serializers import (
    FeedbackTaskSerializer,
    FeedbackTaskCreateSerializer,
    FeedbackTaskUpdateStatusSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_feedback_tasks(request):
    """
    Lấy danh sách tất cả feedback tasks
    Query params:
    - status: Pending hoặc Finished (optional)
    """
    status_filter = request.GET.get('status', None)
    
    tasks = ClinicFeedbackTask.objects.all()
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    serializer = FeedbackTaskSerializer(tasks, many=True)
    
    return Response({
        'success': True,
        'data': serializer.data,
        'count': tasks.count()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_feedback_task(request, pk):
    """Lấy chi tiết 1 feedback task"""
    task = get_object_or_404(ClinicFeedbackTask, pk=pk)
    serializer = FeedbackTaskSerializer(task)
    
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def create_feedback_task(request):
    """
    Tạo feedback task mới (được gọi từ n8n webhook)
    Body: {
        "customer_email": "email@example.com",
        "score_doctor_attitude": "Tốt",
        "score_doctor_clarity": "Có",
        ...
    }
    """
    serializer = FeedbackTaskCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        task = serializer.save()
        response_data = FeedbackTaskSerializer(task).data
        
        return Response({
            'success': True,
            'message': 'Tạo feedback task thành công',
            'data': response_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_task_status(request, pk):
    """
    Cập nhật trạng thái task (Pending -> Finished)
    Body: { "status": "Finished" }
    """
    task = get_object_or_404(ClinicFeedbackTask, pk=pk)
    
    serializer = FeedbackTaskUpdateStatusSerializer(task, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        response_data = FeedbackTaskSerializer(task).data
        
        return Response({
            'success': True,
            'message': 'Cập nhật trạng thái thành công',
            'data': response_data
        })
    
    return Response({
        'success': False,
        'message': 'Dữ liệu không hợp lệ',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_feedback_task(request, pk):
    """Xóa feedback task"""
    task = get_object_or_404(ClinicFeedbackTask, pk=pk)
    task.delete()
    
    return Response({
        'success': True,
        'message': 'Xóa feedback task thành công'
    }, status=status.HTTP_204_NO_CONTENT)
