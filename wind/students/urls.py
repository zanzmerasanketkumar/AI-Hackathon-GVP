from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/report/', views.student_report, name='student_report'),
    path('attendance/', views.attendance_management, name='attendance_management'),
    path('performance/', views.performance_management, name='performance_management'),
]
