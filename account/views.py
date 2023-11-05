from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import make_password
from .serializers import SignUpSerializer, UserSerializer
from django.contrib.auth.models import User

from .validators import validate_file_extensions

# Create your views here.
@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username = data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                username = data['email'],
                email = data['email'],
                password = make_password(data['password'])
            )
            return Response({'detail': 'User registered succesfully', },status = status.HTTP_200_OK)

        else:
            return Response({'detail': 'User already exists',},status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': user.errors})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user

    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['username']
    user.email = data['email']

    if data['password'] != '':
        user.password= make_password(data['password'])

    user.save()
    serializer = UserSerializer(user, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def upload_resume(request):
    user = request.user
    resume = request.FILES['resume']

    # resume = request.POST.get('resume', '')

    if resume == '':
        return Response(
            {'detail': 'Upload your resume'},
            status = status.HTTP_400_BAD_REQUEST
        )
    
    is_valid_file = validate_file_extensions(resume.name)

    if not is_valid_file:
        return Response(
            {'detail': 'Not valid extension, just pdf'},
            status = status.HTTP_400_BAD_REQUEST
        )

    serializer = UserSerializer(user, many=False)

    user.userprofile.resume = resume
    user.userprofile.save()

    return Response(serializer.data)