# Student Management System

A full-stack **Student Management System** developed using **Flask (Python)**, **MySQL**, **HTML/CSS**, and **Jinja2**.  
This application allows administrators to efficiently manage students, courses, subjects, and view summarized dashboard statistics.

---

## 🚀 Features

### 🔐 Authentication
- Admin Login
- Admin Registration
- Forgot Password page (UI implemented)
- Session-based authentication

### 📊 Dashboard
- Total Students count
- Total Courses count
- Total Departments count
- Professional UI with persistent sidebar navigation

### 🎓 Course Management
- Add, edit, delete courses
- Department-wise course structure
- Clickable courses to view subjects

### 📘 Subject Management
- Add, edit, delete subjects
- Assign credits to subjects
- Subjects linked to respective courses

### 👩‍🎓 Student Management
- Add students with complete details:
  - Register Number
  - Name, Age, Gender
  - Father & Mother Name
  - Phone & Email
  - Address
  - Department & Course
- View complete student profile
- Edit student details
- Delete student records

### 🎨 UI & Design
- Modern dashboard layout
- Sidebar remains visible across main pages
- Responsive cards, tables, and forms
- Custom CSS styling for professional appearance

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Jinja2
- **Database:** MySQL
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

Student Management System/
│
├── app.py
├── db.py
├── static/
│ └── css/
│ └── style.css
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── forgot_password.html
│ ├── home.html
│ ├── courses.html
│ ├── subjects.html
│ ├── students.html
│ ├── add_course.html
│ ├── add_subject.html
│ ├── add_students.html
│ ├── edit_course.html
│ ├── edit_subject.html
│ ├── edit_student.html
│ └── view_student.html
└── README.md

## 🗄️ Database Tables

- `admin`
- `course`
- `subject`
- `student`

### Relationships
- `course.course_id` → `subject.course_id`
- `course.course_id` → `student.course_id`

Foreign keys ensure referential integrity.

---

## ▶️ How to Run the Project

1. Clone the repository
   ```bash
   git clone https://github.com/Dharshini1202/student-management-system.git

2. Navigate to the project directory
cd student-management-system

3. Install required packages
pip install flask mysql-connector-python

4. Configure MySQL connection in db.py
   
5. Run the application
python app.py


6. Open in browser
http://127.0.0.1:5000


🔐 Admin Access
Create an admin account using the Register page before logging in.

