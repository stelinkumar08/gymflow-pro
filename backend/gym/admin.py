from django.contrib import admin
from .models import GymProfile, Plan, Member, Payment, SMSLog


# Register your models here.
# Basic registration first -- we'll make it fancy below
@admin.register(GymProfile)
class GymProfileAdmin(admin.ModelAdmin):
    list_display = ['gym_name', 'owner', 'city', 'phone', 'created_at']
    search_fields = ['gym_name', 'owner__username']

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'gym', 'price', 'duration_days', 'is_active']
    list_filter  = ['is_active', 'gym']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'phone', 'plan', 'fee_paid', 'status', 'due_date']
    list_filter   = ['status', 'fee_paid', 'plan']
    search_fields = ['full_name', 'phone', 'email']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['member', 'amount', 'method', 'paid_date']
    list_filter   = ['method']
    search_fields = ['member__full_name']

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['phone', 'status', 'sent_at']
    list_filter  = ['status']