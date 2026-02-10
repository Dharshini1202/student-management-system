from flask import Flask, render_template, request, redirect, session
from db import get_connection

app = Flask(__name__)
app.secret_key = "secret123"


# ==========================
# AUTHENTICATION
# ==========================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM admin WHERE email=%s AND password=%s",
            (email, password)
        )
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin"] = admin["email"]
            return redirect("/home")

        return "Invalid credentials"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM admin WHERE email=%s", (email,))
        if cursor.fetchone():
            conn.close()
            return "Account already exists"

        cursor.execute(
            "INSERT INTO admin (email, password) VALUES (%s,%s)",
            (email, password)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("register.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM admin WHERE email=%s", (email,))
        admin = cursor.fetchone()

        if not admin:
            conn.close()
            return render_template(
                "forgot_password.html",
                message="No account found with this email"
            )

        cursor.execute(
            "UPDATE admin SET password=%s WHERE email=%s",
            (new_password, email)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("forgot_password.html")



@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# ==========================
# DASHBOARD
# ==========================
@app.route("/home")
def home():
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM student")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM course")
    total_courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT department) FROM course")
    total_departments = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "home.html",
        total_students=total_students,
        total_courses=total_courses,
        total_departments=total_departments
    )


# ==========================
# COURSE MODULE
# ==========================

@app.route("/courses")
def courses():
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    conn.close()

    return render_template("courses.html", courses=courses)


@app.route("/add-course", methods=["GET", "POST"])
def add_course():
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        department = request.form["department"]
        course_name = request.form["course_name"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO course (department, course_name) VALUES (%s,%s)",
            (department, course_name)
        )
        conn.commit()
        conn.close()
        return redirect("/courses")

    return render_template("add_course.html")


@app.route("/edit-course/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute(
            "UPDATE course SET department=%s, course_name=%s WHERE course_id=%s",
            (request.form["department"], request.form["course_name"], course_id)
        )
        conn.commit()
        conn.close()
        return redirect("/courses")

    cursor.execute("SELECT * FROM course WHERE course_id=%s", (course_id,))
    course = cursor.fetchone()
    conn.close()

    return render_template("edit_course.html", course=course)


@app.route("/delete-course/<int:course_id>")
def delete_course(course_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM course WHERE course_id=%s", (course_id,))
    conn.commit()
    conn.close()

    return redirect("/courses")


# ==========================
# SUBJECT MODULE
# ==========================

@app.route("/subjects/<int:course_id>")
def subjects(course_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM course WHERE course_id=%s", (course_id,))
    course = cursor.fetchone()

    cursor.execute("SELECT * FROM subject WHERE course_id=%s", (course_id,))
    subjects = cursor.fetchall()

    conn.close()
    return render_template("subjects.html", course=course, subjects=subjects)


@app.route("/add-subject/<int:course_id>", methods=["GET", "POST"])
def add_subject(course_id):
    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO subject (course_id, subject_name, credits) VALUES (%s,%s,%s)",
            (course_id, request.form["subject_name"], request.form["credits"])
        )
        conn.commit()
        conn.close()
        return redirect(f"/subjects/{course_id}")

    return render_template("add_subject.html", course_id=course_id)


@app.route("/edit-subject/<int:subject_id>", methods=["GET", "POST"])
def edit_subject(subject_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            UPDATE subject
            SET subject_name=%s, credits=%s
            WHERE subject_id=%s
        """, (
            request.form["subject_name"],
            request.form["credits"],
            subject_id
        ))

        conn.commit()
        conn.close()
        return redirect("/courses")

    cursor.execute("SELECT * FROM subject WHERE subject_id=%s", (subject_id,))
    subject = cursor.fetchone()
    conn.close()

    return render_template("edit_subject.html", subject=subject)


@app.route("/delete-subject/<int:subject_id>/<int:course_id>")
def delete_subject(subject_id, course_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subject WHERE subject_id=%s", (subject_id,))
    conn.commit()
    conn.close()

    return redirect(f"/subjects/{course_id}")


# ==========================
# STUDENT MODULE
# ==========================

@app.route("/students")
def students():
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.*, c.course_name
        FROM student s
        LEFT JOIN course c ON s.course_id = c.course_id
    """)
    students = cursor.fetchall()

    cursor.execute("""
        SELECT department, COUNT(*) AS total
        FROM student
        GROUP BY department
    """)
    summary = cursor.fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students,
        summary=summary
    )


@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            INSERT INTO student
            (register_number, name, age, sex,
             father_name, mother_name, phone, email,
             address, department, course_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["register_number"],
            request.form["name"],
            request.form["age"],
            request.form["sex"],
            request.form["father_name"],
            request.form["mother_name"],
            request.form["phone"],
            request.form["email"],
            request.form["address"],
            request.form["department"],
            request.form["course_id"]
        ))
        conn.commit()
        conn.close()
        return redirect("/students")

    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    conn.close()

    return render_template("add_students.html", courses=courses)


@app.route("/edit-student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute("""
            UPDATE student SET
            register_number=%s,
            name=%s,
            age=%s,
            sex=%s,
            father_name=%s,
            mother_name=%s,
            phone=%s,
            email=%s,
            address=%s,
            department=%s,
            course_id=%s
            WHERE student_id=%s
        """, (
            request.form["register_number"],
            request.form["name"],
            request.form["age"],
            request.form["sex"],
            request.form["father_name"],
            request.form["mother_name"],
            request.form["phone"],
            request.form["email"],
            request.form["address"],
            request.form["department"],
            request.form["course_id"],
            student_id
        ))
        conn.commit()
        conn.close()
        return redirect("/students")

    cursor.execute("SELECT * FROM student WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()

    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    conn.close()

    return render_template(
        "edit_student.html",
        student=student,
        courses=courses
    )


@app.route("/student/<int:student_id>")
def view_student(student_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.*, c.course_name
        FROM student s
        LEFT JOIN course c ON s.course_id = c.course_id
        WHERE s.student_id=%s
    """, (student_id,))

    student = cursor.fetchone()
    conn.close()

    return render_template("view_student.html", student=student)


@app.route("/delete-student/<int:student_id>")
def delete_student(student_id):
    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE student_id=%s", (student_id,))
    conn.commit()
    conn.close()

    return redirect("/students")


# ==========================
# RUN
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
