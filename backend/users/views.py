from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import UserCreateSerializer, UserSerializer, LoginSerializer
from .models import User
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    API tạo người dùng mới
    """
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
    """
    API lấy danh sách người dùng
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({
        'success': True,
        'data': serializer.data
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    API đăng nhập
    """
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
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    API đăng xuất
    """
    logout(request)
    return Response({
        'success': True,
        'message': 'Đăng xuất thành công'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    API lấy thông tin user hiện tại
    """
    serializer = UserSerializer(request.user)
    return Response({
        'success': True,
        'data': serializer.data
    })
