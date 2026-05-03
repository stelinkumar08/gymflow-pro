from django.db import models
from django.contrib.auth.models import User

#--------------------------------------------
# 1. GYM PROFILE
# Each gym owner has one gym profile.
# We link it to Django's built-in User model.
# Using OneToOneField - one user, one gym
#--------------------------------------------

class GymProfile(models.Model):
    # OneToOneField means: one user = one GymProfile. No more, no less
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,  #if user deleted, delete gym profile too
        related_name='gym_profile'
    )
    gym_name   = models.CharField(max_length=200)
    address    = models.TextField(blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    city       = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)      # set once
    update_at  = models.DateTimeField(auto_now = True)          # updates

    def __str__(self):
        # This controls what you see in Django admin
        return f"{self.gym_name}  ({self.owner.username})"
    
    class Meta:
        verbose_name        = "Gym Profile"
        verbose_name_plural = "Gym Profiles"


#--------------------------------------------
# 2. MEMBERSHIP PLAN
# Each gym creates their own plans.
# Basics, Standard, Premium - with their own prices.
#--------------------------------------------

class Plan(models.Model):
    # ForeignKey means: one GymProfile can have MANY Plans
    gym    = models.ForeignKey(
        GymProfile,
        on_delete    = models.CASCADE,
        related_name = 'plans'         #gym.plans.all() gives all plans for a gym 
    )
    name          = models.CharField(max_length = 100)                       # "Premium"
    price         = models.DecimalField(max_digits = 8, decimal_places = 2)  # 1999.00
    duration_days = models.IntegerField(default = 30)                        # How many days it lasts
    description   = models.TextField(blank = True)
    is_active     = models.BooleanField(default = True)
    created_at    = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.name} - ₹{self.price} ({self.gym.gym_name})"
    
    class Meta:
        ordering = ['price']  # always return plan cheapest to most expensive

#-----------------------------------------------
# 3. MEMBER
# The most important table in the whole app.
#-----------------------------------------------

class Member(models.Model):

    # Status choices - never use raw string scattered in your code.
    # Always define choices as constants in the model. This is the
    # proffessional way. If you need to change "active" to "ACTIVE"
    # later, you change it in ONE place only.
    class Status(models.TextChoices):
        ACTIVE   = 'active',   'Active'
        INACTIVE = 'inactive', 'Inactive'
        FROZEN   = 'frozen',   'Frozen'

    gym = models.ForeignKey(
        GymProfile,
        on_delete = models.CASCADE,
        related_name = 'members'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete    = models.SET_NULL,  # if plan deleted, keep number but set plan to null
        null         = True,
        blank        = True,
        related_name = 'members'
    )

    # Personal info
    full_name   = models.CharField(max_length = 200)
    phone       = models.CharField(max_length = 20, unique = True)
    email       = models.EmailField(blank = True)
    address     = models.TextField(blank = True)

    # Membership info
    join_data   = models.DateField(auto_now_add = True)
    due_date    = models.DateField(null = True, blank = True)
    status      = models.CharField(
        max_length = 20,
        choices = Status.choices,
        default = Status.ACTIVE
    )

    # Fee Tracking
    fee_amount  = models.DecimalField(max_digits = 8, decimal_places = 2)
    fee_paid    = models.BooleanField(default = False)

    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def __str__ (self):
        return f"{self.full_name} - {self.phone}"
    
    class Meta:
        ordering = ['-created_at']   # newest member first

#---------------------------------------------------------
# 4. PAYMENT
# Every time a member pays. we record it here.
# Never delete payment records - this is financial data.
#---------------------------------------------------------

class Payment(models.Model):

    class PaymentMethod(models.TextChoices):
        CASH  = 'cash', 'Cash'
        UPI   = 'upi', 'UPI'
        CARD  = 'card', 'Card'
        BANK  = 'bank', 'Bank Transfer'
        OTHER = 'other', 'Other'

    member = models.ForeignKey(
        Member,
        on_delete = models.PROTECT,  #PROTECT = never delete member if payment exist
        related_name = 'payments'
    )
    amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    method = models.CharField(
        max_length = 20,
        choices = PaymentMethod.choices,
        default = PaymentMethod.CASH
    )
    paid_date  = models.DateField(auto_now_add = True)
    notes      = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__ (self):
        return f"₹{self.amount} from {self.member.full_name} on {self.paid_date}"
    
    class Meta:
        ordering = ['-paid_date']

#------------------------------------------------
# 5. SMS LOG
# Every SMS we send gets recorded here.
# Usefull for tracking, debugging, and avoiding spam.
#------------------------------------------------

class SMSLog (models.Model):
    
    class SMSStatus (models.TextChoices):
        SENT    = 'sent', 'Sent'
        FAILED  = 'failed', 'Failed'
        PENDING = 'pending', 'Pending'
    
    member = models.ForeignKey(
        Member,
        on_delete    = models.CASCADE,
        related_name = 'sms_logs'
    )
    phone   = models.CharField(max_length = 20) # stores phone at time of sending
    message = models.TextField()
    status  = models.CharField(
        max_length = 20,
        choices = SMSStatus.choices,
        default = SMSStatus.PENDING
    )
    sent_at   = models.DateTimeField(auto_now_add = True)
    error_msg = models.TextField(blank = True)    # store error is SMS failed

    def __str__ (self):
        return f"SMS to {self.phone} - {self.status}"
    
    class Meta:
        ordering = ['-sent_at']