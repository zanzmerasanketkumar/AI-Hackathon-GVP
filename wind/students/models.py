from django.db import models
from django.utils import timezone
import datetime

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    PROGRAM_CHOICES = [
        ('MCA', 'Master of Computer Applications'),
        ('MScIT', 'Master of Science in Information Technology'),
        ('BCA', 'Bachelor of Computer Applications'),
        ('PGDCA', 'Post Graduate Diploma in Computer Applications'),
    ]
    
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Contact Information
    phone_number = models.CharField(max_length=15, help_text="Include country code")
    personal_email = models.EmailField(max_length=100, help_text="Personal email address")
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='India')
    
    # Academic Information
    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    
    # Physical Information
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relation = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=15)
    
    # System Generated Fields
    student_id = models.CharField(max_length=10, unique=True, editable=False)
    email_id = models.EmailField(max_length=50, unique=True, editable=False)
    admission_year = models.IntegerField(editable=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-student_id']
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def name(self):
        return self.full_name
    
    def __str__(self):
        return f"{self.full_name} ({self.student_id})"
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = self.generate_student_id()
            self.email_id = self.generate_email_id()
            self.admission_year = datetime.datetime.now().year
        super().save(*args, **kwargs)
    
    def generate_student_id(self):
        current_year = datetime.datetime.now().year
        year_suffix = str(current_year)[-2:]
        
        program_codes = {
            'MCA': 101,
            'MScIT': 201,
            'BCA': 301,
            'PGDCA': 401,
        }
        
        base_code = program_codes.get(self.program, 101)
        
        last_student = Student.objects.filter(
            program=self.program,
            admission_year=current_year
        ).order_by('-student_id').first()
        
        if last_student:
            last_number = int(last_student.student_id[-3:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"{year_suffix}{base_code + new_number:03d}"
    
    def generate_email_id(self):
        return f"{self.student_id}.gvp@gujaratvidyapith.org"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.name} - {self.date} - {'Present' if self.is_present else 'Absent'}"


class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performances')
    subject = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField(default=100)
    exam_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-exam_date']
    
    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.marks_obtained}/{self.total_marks}"
    
    @property
    def percentage(self):
        if self.total_marks > 0:
            return round((self.marks_obtained / self.total_marks) * 100, 2)
        return 0
    
    @property
    def remark(self):
        percentage = self.percentage
        if percentage >= 75:
            return "Good"
        elif percentage >= 50:
            return "Average"
        else:
            return "Needs Improvement"
