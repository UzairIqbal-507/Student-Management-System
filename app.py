import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from database import (
    init_db,
    db_get_all_students,
    db_get_student_by_id,
    db_add_student,
    db_update_student,
    db_delete_student,
    db_authenticate_user,
    db_register_user
)
from utils import (
    get_academic_summary,
    get_student_performance_report,
    export_student_performance_pdf
)
from validation import calculate_result

app = Flask(__name__)
app.secret_key = "student_management_secret_key"

# Initialize Database & Default Admin Account
init_db()

# AUTHENTICATION DECORATORS
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in first to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session or session["user"].get("role") != "admin":
            flash("Access denied! Admin permissions required.", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

# AUTHENTICATION ROUTES
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user = db_authenticate_user(username, password)
        if user:
            session["user"] = {
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "student_id": user.get("student_id")
            }
            flash(f"Welcome back, {user['username']}! 👋", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username/email or password! ❌", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        role = request.form.get("role", "student")
        student_id = request.form.get("student_id", "").strip() or None

        success, msg = db_register_user(username, email, password, role, student_id)
        if success:
            flash("Account registered successfully! Please log in. ✅", "success")
            return redirect(url_for("login"))
        else:
            flash(f"Registration failed: Username or Email might exist! ❌", "danger")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# 1. HOME / VIEW ALL
@app.route("/")
@login_required
def index():
    user_role = session["user"]["role"]
    if user_role == "student" and session["user"].get("student_id"):
        # Students see only their own record
        student = db_get_student_by_id(session["user"]["student_id"])
        students = [student] if student else []
    else:
        students = db_get_all_students()

    return render_template("index.html", students=students, current_user=session.get("user"))

# 2. ADD STUDENT (ADMIN ONLY)
@app.route("/add", methods=["GET", "POST"])
@admin_required
def add_student():
    if request.method == "POST":
        students = db_get_all_students()
        student_id = request.form.get("student_id").strip()

        for student in students:
            if student["student_id"] == student_id:
                flash("Student ID already exists! ❌", "danger")
                return redirect(url_for("add_student"))

        # DYNAMIC MARKS EXTRACTION (Form se saare 'marks[SubjectName]' keys pick karega)
        marks = {}
        for key in request.form:
            if key.startswith("marks[") and key.endswith("]"):
                subject_name = key[6:-1]
                val = request.form.get(key, 0)
                marks[subject_name] = float(val) if val else 0.0

        # Agar dynamic format nah mila toh fallback standard fields se uthayega
        if not marks:
            default_subjects = ["Python", "DBMS", "Statistics", "Mathematics", "Calculus", "DLD"]
            for sub in default_subjects:
                val = request.form.get(sub.lower(), 0)
                if val:
                    marks[sub] = float(val)

        total_marks, maximum_marks, percentage, grade = calculate_result(marks)

        new_student = {
            "student_id": student_id,
            "name": request.form.get("name").strip(),
            "email": request.form.get("email").strip(),
            "phone": request.form.get("phone").strip(),
            "department": request.form.get("department"),
            "semester": int(request.form.get("semester")),
            "CGPA": float(request.form.get("cgpa")),
            "marks": marks,
            "total_marks": total_marks,
            "maximum_marks": maximum_marks,
            "percentage": percentage,
            "grade": grade,
        }

        db_add_student(new_student)
        flash("Student added successfully! ✅", "success")
        return redirect(url_for("index"))

    return render_template("add.html")

# 3. UPDATE STUDENT (ADMIN ONLY)
@app.route("/update/<student_id>", methods=["GET", "POST"])
@admin_required
def update_student(student_id):
    target_student = db_get_student_by_id(student_id)

    if not target_student:
        flash("Student not found! ❌", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        target_student["name"] = request.form.get("name").strip()
        target_student["email"] = request.form.get("email").strip()
        target_student["phone"] = request.form.get("phone").strip()
        target_student["department"] = request.form.get("department")
        target_student["semester"] = int(request.form.get("semester"))
        target_student["CGPA"] = float(request.form.get("cgpa"))

        # Dynamic Marks Extraction
        marks = {}
        for key in request.form:
            if key.startswith("marks[") and key.endswith("]"):
                subject_name = key[6:-1]
                val = request.form.get(key, 0)
                marks[subject_name] = float(val) if val else 0.0

        if not marks:
            default_subjects = ["Python", "DBMS", "Statistics", "Mathematics", "Calculus", "DLD"]
            for sub in default_subjects:
                val = request.form.get(sub.lower(), 0)
                if val:
                    marks[sub] = float(val)

        total_marks, maximum_marks, percentage, grade = calculate_result(marks)
        target_student["marks"] = marks
        target_student["total_marks"] = total_marks
        target_student["maximum_marks"] = maximum_marks
        target_student["percentage"] = percentage
        target_student["grade"] = grade

        db_update_student(target_student)
        flash("Student updated successfully! ✅", "success")
        return redirect(url_for("index"))

    return render_template("update.html", student=target_student)

# 4. DELETE STUDENT (ADMIN ONLY)
@app.route("/delete/<student_id>")
@admin_required
def delete_student(student_id):
    student = db_get_student_by_id(student_id)
    if not student:
        flash("Student not found! ❌", "danger")
    else:
        db_delete_student(student_id)
        flash("Student deleted successfully! 🗑️", "warning")

    return redirect(url_for("index"))

# 5. SEARCH
@app.route("/search")
@login_required
def search():
    students = db_get_all_students()
    query = request.args.get("query", "").strip().lower()
    search_by = request.args.get("search_by", "all")

    filtered = []
    if query:
        for s in students:
            if search_by == "id" and query in s["student_id"].lower():
                filtered.append(s)
            elif search_by == "name" and query in s["name"].lower():
                filtered.append(s)
            elif search_by == "department" and query in s["department"].lower():
                filtered.append(s)
            elif search_by == "all":
                if (query in s["student_id"].lower() or
                    query in s["name"].lower() or
                    query in s["department"].lower()):
                    filtered.append(s)
    else:
        filtered = students

    return render_template("search.html", students=filtered, query=query, search_by=search_by)

# 6. DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    students = db_get_all_students()

    if not students:
        chart_data = {
            "departments": [], "department_counts": [],
            "grades": [], "grade_counts": [],
            "subjects": [], "subject_averages": []
        }
        return render_template("dashboard.html", summary=None, chart_data=chart_data)

    summary = get_academic_summary(students)
    dept_counts = summary.get("department_counts", {})
    grade_counts = summary.get("grade_counts", {})
    subj_averages = summary.get("subject_averages", {})

    chart_data = {
        "departments": list(dept_counts.keys()),
        "department_counts": list(dept_counts.values()),
        "grades": list(grade_counts.keys()),
        "grade_counts": list(grade_counts.values()),
        "subjects": list(subj_averages.keys()),
        "subject_averages": [round(val, 2) for val in subj_averages.values()]
    }

    return render_template("dashboard.html", summary=summary, chart_data=chart_data)

# 7. EXPORT PDF REPORT
@app.route("/pdf/<student_id>")
@login_required
def generate_pdf(student_id):
    student = db_get_student_by_id(student_id)
    if not student:
        flash("Student not found! ❌", "danger")
        return redirect(url_for("index"))

    report = get_student_performance_report(student)
    export_student_performance_pdf(report)

    reports_dir = "reports"
    files = [os.path.join(reports_dir, f) for f in os.listdir(reports_dir) if f.startswith(student_id)]
    latest_file = max(files, key=os.path.getctime)
    return send_file(latest_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)