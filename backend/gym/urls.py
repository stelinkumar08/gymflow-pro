from django.urls import path
from . import views
urlpatterns = [
    path('health/', views.health_check),
    path('members/', views.member_list),
    path('members/<int:pk>/', views.member_detail),
    path('plans/', views.plan_list),
    path('payments/', views.payment_list),
]

