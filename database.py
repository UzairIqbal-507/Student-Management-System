import psycopg2
from psycopg2.extras import RealDictCursor, Json
from werkzeug.security import generate_password_hash, check_password_hash
import json

DB_CONFIG = {
    "dbname": "student_db",
    "user": "postgres",
    "password": "Uz@ir507",  # Verify your password
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Departments Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            );
        ''')

        # 2. Subjects Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id SERIAL PRIMARY KEY,
                department_name VARCHAR(100) REFERENCES departments(name) ON DELETE CASCADE,
                subject_name VARCHAR(100) NOT NULL,
                UNIQUE(department_name, subject_name)
            );
        ''')

        # 3. Students Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone VARCHAR(20) NOT NULL UNIQUE,
                department VARCHAR(100) NOT NULL,
                semester INT NOT NULL,
                cgpa NUMERIC(3, 2) NOT NULL,
                marks_json JSONB,
                total_marks NUMERIC(6, 2),
                maximum_marks NUMERIC(6, 2),
                percentage NUMERIC(5, 2),
                grade VARCHAR(10)
            );
        ''')

        # 4. Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'student',
                student_id VARCHAR(50) REFERENCES students(student_id) ON DELETE CASCADE
            );
        ''')

        # 5. Audit Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                action VARCHAR(100) NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        conn.commit()

        # Seed Default Departments & Subjects if empty
        cursor.execute("SELECT COUNT(*) FROM departments;")
        if cursor.fetchone()["count"] == 0:
            default_depts = ["Computer Science", "Data Science", "Software Engineering", "Information Technology"]
            default_subjects = {
                "Computer Science": ["Programming Fundamentals", "Data Structures", "Algorithms", "Operating Systems"],
                "Data Science": ["Python Programming", "Statistics & Probability", "Machine Learning", "Data Mining"],
                "Software Engineering": ["Software Architecture", "Agile Methodologies", "Software Testing", "DBMS"],
                "Information Technology": ["Computer Networks", "Cyber Security", "Cloud Computing", "Web Technologies"]
            }
            for dept in default_depts:
                cursor.execute("INSERT INTO departments (name) VALUES (%s) ON CONFLICT DO NOTHING;", (dept,))
                for sub in default_subjects.get(dept, []):
                    cursor.execute("INSERT INTO subjects (department_name, subject_name) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (dept, sub))
            conn.commit()

        # Default Admin Account
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin';")
        if cursor.fetchone()["count"] == 0:
            admin_pass = generate_password_hash("admin123")
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s);
            ''', ("admin", "admin@school.com", admin_pass, "admin"))
            conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database Init Error: {e}")

# DYNAMIC DEPARTMENTS & SUBJECTS FUNCTIONS
def db_get_all_departments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments ORDER BY name ASC;")
        depts = cursor.fetchall()
        cursor.close()
        conn.close()
        return [d["name"] for d in depts]
    except Exception as e:
        print(f"Fetch Depts Error: {e}")
        return []

def db_get_department_subjects():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects ORDER BY department_name, subject_name;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        dept_sub_map = {}
        for r in rows:
            dept = r["department_name"]
            sub = r["subject_name"]
            if dept not in dept_sub_map:
                dept_sub_map[dept] = []
            dept_sub_map[dept].append(sub)
        return dept_sub_map
    except Exception as e:
        print(f"Fetch Dept Subjects Error: {e}")
        return {}

def db_add_department(dept_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO departments (name) VALUES (%s);", (dept_name,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Department added successfully!"
    except Exception as e:
        return False, str(e)

def db_add_subject(dept_name, subject_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subjects (department_name, subject_name) VALUES (%s, %s);", (dept_name, subject_name))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Subject added successfully!"
    except Exception as e:
        return False, str(e)

def db_delete_department(dept_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM departments WHERE name = %s;", (dept_name,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Delete Dept Error: {e}")
        return False

def db_delete_subject(dept_name, subject_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subjects WHERE department_name = %s AND subject_name = %s;", (dept_name, subject_name))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Delete Subject Error: {e}")
        return False

# AUDIT LOG HELPER
def db_log_action(username, action, details=""):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audit_logs (username, action, details)
            VALUES (%s, %s, %s);
        ''', (username, action, details))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Logging Error: {e}")

def db_get_audit_logs(limit=50):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT %s;", (limit,))
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(log) for log in logs]
    except Exception as e:
        print(f"Fetch Logs Error: {e}")
        return []

# AUTH FUNCTIONS
def db_register_user(username, email, password, role="student", student_id=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_pw = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, student_id)
            VALUES (%s, %s, %s, %s, %s);
        ''', (username, email, hashed_pw, role, student_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "User registered successfully!"
    except Exception as e:
        return False, str(e)

def db_authenticate_user(username_or_email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT * FROM users WHERE username = %s OR email = %s;
        ''', (username_or_email, username_or_email))
        user = cursor.fetchone()
        if user and check_password_hash(user["password_hash"], password):
            return dict(user)
        return None
    finally:
        cursor.close()
        conn.close()

def db_change_password(username, old_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password_hash FROM users WHERE username = %s;", (username,))
        user = cursor.fetchone()
        if not user or not check_password_hash(user["password_hash"], old_password):
            return False, "Current password is incorrect! ❌"

        new_hashed = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s;", (new_hashed, username))
        conn.commit()
        return True, "Password updated successfully! ✅"
    except Exception as e:
        return False, f"Password change failed: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# STUDENT CRUD FUNCTIONS
def db_get_all_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # raw string r""" ... """ used here to eliminate Python SyntaxWarning
        cursor.execute(r"""
            SELECT * FROM students 
            ORDER BY NULLIF(regexp_replace(student_id, '\D', '', 'g'), '')::INT ASC, student_id ASC;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        students = []
        for r in rows:
            s_dict = dict(r)
            raw_cgpa = s_dict.pop("cgpa")
            s_dict["CGPA"] = float(raw_cgpa) if raw_cgpa is not None else 0.0
            s_dict["percentage"] = float(s_dict["percentage"]) if s_dict.get("percentage") is not None else None
            s_dict["total_marks"] = float(s_dict["total_marks"]) if s_dict.get("total_marks") is not None else None
            s_dict["maximum_marks"] = float(s_dict["maximum_marks"]) if s_dict.get("maximum_marks") is not None else None

            marks_data = s_dict.pop("marks_json")
            if isinstance(marks_data, str):
                s_dict["marks"] = json.loads(marks_data)
            else:
                s_dict["marks"] = marks_data or {}

            students.append(s_dict)
        return students
    except Exception as e:
        print(f"Fetch Error: {e}")
        return []

def db_get_student_by_id(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s;", (student_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            s_dict = dict(row)
            raw_cgpa = s_dict.pop("cgpa")
            s_dict["CGPA"] = float(raw_cgpa) if raw_cgpa is not None else 0.0
            s_dict["percentage"] = float(s_dict["percentage"]) if s_dict.get("percentage") is not None else None
            s_dict["total_marks"] = float(s_dict["total_marks"]) if s_dict.get("total_marks") is not None else None
            s_dict["maximum_marks"] = float(s_dict["maximum_marks"]) if s_dict.get("maximum_marks") is not None else None

            marks_data = s_dict.pop("marks_json")
            if isinstance(marks_data, str):
                s_dict["marks"] = json.loads(marks_data)
            else:
                s_dict["marks"] = marks_data or {}

            return s_dict
        return None
    except Exception as e:
        print(f"Fetch Single Error: {e}")
        return None

def db_add_student(student):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students 
        (student_id, name, email, phone, department, semester, cgpa, marks_json, total_marks, maximum_marks, percentage, grade)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    ''', (
        student["student_id"],
        student["name"],
        student["email"],
        student["phone"],
        student["department"],
        student["semester"],
        student["CGPA"],
        Json(student.get("marks", {})),
        student.get("total_marks"),
        student.get("maximum_marks"),
        student.get("percentage"),
        student.get("grade")
    ))
    conn.commit()
    cursor.close()
    conn.close()

def db_update_student(student):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students
        SET name = %s, email = %s, phone = %s, department = %s, semester = %s, cgpa = %s,
            marks_json = %s, total_marks = %s, maximum_marks = %s, percentage = %s, grade = %s
        WHERE student_id = %s;
    ''', (
        student["name"],
        student["email"],
        student["phone"],
        student["department"],
        student["semester"],
        student["CGPA"],
        Json(student.get("marks", {})),
        student.get("total_marks"),
        student.get("maximum_marks"),
        student.get("percentage"),
        student.get("grade"),
        student["student_id"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

def db_delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()