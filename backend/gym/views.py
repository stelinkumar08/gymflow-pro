from django.shortcuts import render
from .serializers import MemberSerializer
from .models import Member

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        'status': 'GymFlow API is running!',
        'version': '1.0'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def member_list(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)