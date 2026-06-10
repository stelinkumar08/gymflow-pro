from rest_framework import serializers #importing srealizer from rest framework
from .models import Member, Plan #importing Member class from models.py in gym


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['name', 'price']
class MemberSerializer(serializers.ModelSerializer): #creating a class called MemberSerializer. In that bracet importing two of the called models.
    plan = PlanSerializer()
    class Meta: #creating a second class in Main class
        model = Member #adding Member to model
        fields = ['id', 'full_name', 'phone', 'plan', 'fee_amount', 'fee_paid', 'status', 'due_date'] #Now seperating the Member values in fields.


