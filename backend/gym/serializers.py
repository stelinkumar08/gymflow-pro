from rest_framework import serializers #importing srealizer from rest framework
from .models import Member, Payment, Plan #importing Member class from models.py in gym

class PlanSerializer(serializers.ModelSerializer): #creating a class called PlanSerializer. In that bracet importing two of the called models.
    class Meta: #creating a second class in Main class
        model = Plan #adding Plan to model
        fields = ['name', 'gym', 'price'] #Now seperating the Plan values in fields.
class MemberSerializer(serializers.ModelSerializer): #creating a class called MemberSerializer. In that bracet importing two of the called models.
    gym = serializers.PrimaryKeyRelatedField(read_only=True) #creating a gym variable and assigning it to PrimaryKeyRelatedField and making it read only.
    plan = PlanSerializer(read_only=True) #creating a plan variable and assigning it to PlanSerializer and making it read only.
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all(), source='plan', write_only=True) #creating a plan_id variable and assigning it to PrimaryKeyRelatedField and making it write only.
    class Meta: #creating a second class in Main class
        model = Member #adding Member to model
        fields = ['id', 'gym', 'full_name', 'phone', 'plan', 'plan_id', 'fee_amount', 'fee_paid', 'status', 'due_date'] #Now seperating the Member values in fields.

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'member', 'amount', 'method', 'paid_date', 'notes']
