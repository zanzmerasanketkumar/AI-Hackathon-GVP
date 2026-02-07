from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Student, Attendance, Performance
from .forms import StudentForm, AttendanceForm, PerformanceForm


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('admin_login')


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_login')
    
    total_students = Student.objects.count()
    total_attendance_today = Attendance.objects.filter(date=timezone.now().date()).count()
    recent_students = Student.objects.order_by('-created_at')[:5]
    
    # Additional admin statistics
    total_attendance_records = Attendance.objects.count()
    total_performance_records = Performance.objects.count()
    
    # Program-wise student count
    program_stats = Student.objects.values('program').annotate(count=Count('id'))
    
    context = {
        'total_students': total_students,
        'total_attendance_today': total_attendance_today,
        'recent_students': recent_students,
        'total_attendance_records': total_attendance_records,
        'total_performance_records': total_performance_records,
        'program_stats': program_stats,
    }
    return render(request, 'admin_dashboard.html', context)


def student_list(request):
    students = Student.objects.all().order_by('-student_id')
    return render(request, 'students/student_list.html', {'students': students})


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} created successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'students/student_form_detailed.html', {'form': form, 'title': 'Add Student'})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    attendance_data = student.attendances.all().order_by('-date')
    total_classes = attendance_data.count()
    present_classes = attendance_data.filter(is_present=True).count()
    absent_classes = total_classes - present_classes
    attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
    
    performances = student.performances.all().order_by('-exam_date')
    average_marks = performances.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    
    context = {
        'student': student,
        'attendance_data': attendance_data,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'absent_classes': absent_classes,
        'attendance_percentage': attendance_percentage,
        'performances': performances,
        'average_marks': round(average_marks, 2),
    }
    return render(request, 'students/student_detail.html', context)


def attendance_management(request):
    # Group students by batch (program + admission year)
    students = Student.objects.all().order_by('program', 'admission_year', 'student_id')
    batches = {}
    
    for student in students:
        batch_key = f"{student.program}{student.admission_year}"
        batch_name = f"{student.get_program_display()} {student.admission_year}"
        
        if batch_key not in batches:
            batches[batch_key] = {
                'code': batch_key,
                'name': batch_name,
                'program': student.program,
                'year': student.admission_year,
                'count': 0
            }
        batches[batch_key]['count'] += 1
    
    # Convert to list and sort by program and year
    batch_list = list(batches.values())
    batch_list.sort(key=lambda x: (x['program'], x['year']))
    
    if request.method == 'POST':
        date = request.POST.get('date')
        if not date:
            messages.error(request, 'Please select a date')
            return redirect('attendance_management')
        
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        students = Student.objects.all()
        
        for student in students:
            attendance_key = f'attendance_{student.pk}'
            is_present = request.POST.get(attendance_key) == 'present'
            
            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'is_present': is_present}
            )
        
        messages.success(request, f'Attendance for {selected_date} has been marked successfully!')
        return redirect('attendance_management')
    
    context = {
        'students': students,
        'batches': batch_list
    }
    return render(request, 'attendance/attendance_management.html', context)


def performance_management(request):
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            performance = form.save()
            messages.success(request, f'Performance record for {performance.student.name} added successfully!')
            return redirect('student_detail', pk=performance.student.pk)
    else:
        form = PerformanceForm()
    
    performances = Performance.objects.all().order_by('-exam_date')
    return render(request, 'performance/performance_management.html', {
        'form': form,
        'performances': performances
    })


def student_report(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    attendance_data = student.attendances.all().order_by('-date')
    total_classes = attendance_data.count()
    present_classes = attendance_data.filter(is_present=True).count()
    absent_classes = total_classes - present_classes
    attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
    
    performances = student.performances.all().order_by('-exam_date')
    average_marks = performances.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
    
    # Calculate performance counts using the remark property
    good_count = sum(1 for p in performances if p.remark == 'Good')
    average_count = sum(1 for p in performances if p.remark == 'Average')
    needs_improvement_count = sum(1 for p in performances if p.remark == 'Needs Improvement')
    
    attendance_warning = attendance_percentage < 75
    
    context = {
        'student': student,
        'attendance_data': attendance_data,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'absent_classes': absent_classes,
        'attendance_percentage': attendance_percentage,
        'performances': performances,
        'average_marks': round(average_marks, 2),
        'attendance_warning': attendance_warning,
        'good_count': good_count,
        'average_count': average_count,
        'needs_improvement_count': needs_improvement_count,
    }
    return render(request, 'reports/student_report.html', context)
