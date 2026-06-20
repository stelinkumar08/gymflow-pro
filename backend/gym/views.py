import re
import stat
from urllib import request

from django.shortcuts import render
from .serializers import MemberSerializer, PlanSerializer, PaymentSerializer
from .models import Member, Plan, Payment

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


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def member_list(request):
    if request.method == 'GET':
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def member_detail(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=404)

    if request.method == 'GET':
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        member.delete()
        return Response({'message': 'Member deleted successfully'}, status=200)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def plan_list(request):
    if request.method == 'GET':
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def payment_list(request):
    if request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)