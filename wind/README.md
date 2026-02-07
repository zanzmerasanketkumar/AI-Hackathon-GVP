# AI-Assisted Smart Attendance & Performance Tracker

A secure, web-based academic management system built using Python (Django) for backend logic and HTML, CSS (Bootstrap), and JavaScript for the responsive frontend.

## 🌍 Real-World Project Definition

AI-Assisted Smart Attendance & Performance Tracker replaces manual registers and scattered spreadsheets used in colleges for managing student attendance and internal assessment. It centralizes student data, automates calculations, and provides intelligent insights such as attendance shortages and performance remarks using AI-assisted logic.

The application follows a **secure login → admin dashboard → student profile/report workflow**, just like real institutional ERP systems.

## 🔐 Authentication & System Flow

When the system starts, the **Login Page** is shown first.

Only the admin can access the system.

**Default Credentials (for system access):**
- **Username:** admin
- **Password:** admin123

*Note: Credentials are not displayed on the login page for security reasons.*

After successful login:
➡ The admin is redirected to the Profile/Dashboard page.
➡ From the dashboard, the admin can navigate to student management, attendance, marks, and reports.

This ensures authorized access and mimics real-world academic portals.

## 🧩 Core System Modules

### 1) Student Management (Admin Controlled)

While adding a student, the system automatically generates:

#### ✅ Student ID Generation Logic

- **First 2 digits** → Admission Year (e.g., 2026 → 26)
- **Next 3 digits** → Program Code

| Program | Code Starts From |
|---------|------------------|
| MCA     | 101              |
| MScIT   | 201              |
| BCA     | 301              |
| PGDCA   | 401              |

**Example:**
- First MCA student in 2026 → 260101
- Second MCA student → 260102

#### ✅ Automatic Email ID Creation

From Student ID:

**Format:** `<studentid>.gvp@gujaratvidyapith.org`

**Example:** 260101.gvp@gujaratvidyapith.org

### 2) Attendance Management

- Mark Present/Absent
- Automatic attendance percentage calculation
- ⚠ Warning shown if attendance < 75%

### 3) Performance (Marks) Management

- Enter marks (out of 100)
- Calculate average
- AI-generated remark:
  - ≥ 75 → Good
  - 50–74 → Average
  - < 50 → Needs Improvement

### 4) Student Report Dashboard

Report displays:
- Student ID
- Auto-generated Email ID
- Attendance %
- Marks
- Performance remark
- Attendance warning (if any)

## 🤖 AI-Assisted Features

AI tools were used to:
- Design Student ID and email generation logic
- Generate validation rules
- Create attendance warning logic
- Create performance remark logic
- Generate sample test data
- Speed up Django development

## 🛠 Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Django |
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Database | SQLite / MySQL |
| AI Support | AI tools for validation, logic, and testing |

## 🎯 Real-World Use Case

Applicable for:
- Colleges
- Universities
- Coaching institutes
- Training centers

This system works like a mini academic ERP with authentication, automated student credentials, and smart performance tracking.

## ✅ Key Benefits

- Secure login system
- Automatic Student ID & Email generation
- Eliminates manual calculation errors
- Centralized academic data
- Instant insights on attendance & performance
- AI-assisted logic implementation
- Clean and responsive Bootstrap interface

## 🧪 Expected Outcome

A working Django web application where:
- Admin logs in → redirected to dashboard
- Admin adds students → system auto-generates ID & email
- Admin marks attendance and enters marks
- System shows attendance %, remarks, and warnings
- Reports are visible in a structured dashboard

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd attendance_tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Login page: `http://localhost:8000`
   - Admin dashboard: `http://localhost:8000/admin-dashboard/`

## 🚀 Quick Start Guide

### 1. Login to System
- Go to `http://localhost:8000`
- Use credentials: **admin / admin123**
- You'll be redirected to admin dashboard

### 2. Add Students
- Navigate to "Add Student" from the dashboard
- Fill in student details (name, program, semester)
- System automatically generates Student ID and Email ID

### 3. Mark Attendance
- Go to "Attendance Management"
- Select date and mark present/absent for all students
- System calculates attendance percentages automatically

### 4. Record Performance
- Access "Performance Management"
- Enter marks for different subjects
- AI generates performance remarks automatically

### 5. Generate Reports
- Click "Generate Report" on any student page
- View comprehensive academic performance report
- Print or save reports for documentation

## 📊 Student ID Generation Logic

### Format: `YY + Program Code + Sequence Number`

**Example:**
- First MCA student in 2026: `260101`
- Email ID: `260101.gvp@gujaratvidyapith.org`

### Program Codes:
- **MCA**: 101 (Master of Computer Applications)
- **MScIT**: 201 (Master of Science in Information Technology)
- **BCA**: 301 (Bachelor of Computer Applications)
- **PGDCA**: 401 (Post Graduate Diploma in Computer Applications)

## � UI/UX Features

- **Modern Bootstrap Interface**: Clean, professional design
- **Secure Login System**: Authentication-first approach
- **Interactive Dashboard**: Real-time statistics and quick actions
- **Color-coded Performance**: Visual indicators for performance levels
- **Print-Ready Reports**: Professional formatting for documentation
- **Mobile-Friendly**: Optimized for all device sizes

## 🔒 Security Features

- **Admin-Only Access**: Secure authentication system
- **CSRF Protection**: Built-in Django security
- **Session Management**: Secure login/logout functionality
- **Input Validation**: Form data validation and sanitization

## � System Workflow

1. **System Start** → Login Page
2. **Admin Login** → Dashboard Redirect
3. **Dashboard** → Student Management Options
4. **Student Operations** → Add/View/Manage Students
5. **Attendance & Performance** → Data Entry & Tracking
6. **Reports** → Generate Academic Insights

---

**Developed with ❤️ using Django and modern web technologies**
