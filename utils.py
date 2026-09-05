import json
import os
import csv
import pandas as pd
import json
from datetime import datetime
from openpyxl import Workbook

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

#LOAD STUDENTS FROM FILE
#============================
def load_students():
    try:
        with open('students.json') as json_file:
            return json.load(json_file)

    except FileNotFoundError:
        return []

#SAVE STUDENTS DATA INTO FILE
#=========================
def save_students(students):

    if os.path.exists('students.json'):
        backup_students()

    with open('students.json', 'w') as json_file:
        json.dump(students, json_file, indent=4)



# BACKUP STUDENTS DATA
# =========================
def backup_students():
    try:
        with open('students.json') as source:
            students = json.load(source)

        os.makedirs('backups', exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        backup_file = f"backups/students_backup_{timestamp}.json"

        with open(backup_file, 'w') as backup:
            json.dump(students, backup, indent=4)

        print(f"\nStudent data backup created: {backup_file} ✅")

    except FileNotFoundError:
        print("\nNo student data available for backup. ❌")

# GET AVAILABLE BACKUPS
# =========================
def get_backups():
    if not os.path.exists("backups"):
        return []

    backups = []

    for file in os.listdir("backups"):
        if file.startswith("students_backup_") and file.endswith(".json"):
            backups.append(file)

    return sorted(backups)

# RESTORE STUDENTS DATA
# =========================
def restore_students(backup_file):
    try:
        backup_path = os.path.join("backups", backup_file)
        if os.path.exists("students.json"):
            backup_students()
        with open(backup_path) as backup:
            students = json.load(backup)

        if not isinstance(students, list):
            print("\nInvalid backup data. ❌")
            return

        with open("students.json", "w") as json_file:
            json.dump(students, json_file, indent=4)

        print("\nStudent data restored successfully. ✅")

    except (FileNotFoundError, json.JSONDecodeError):
        print("\nUnable to restore this backup. ❌")

# EXPORT STUDENTS TO CSV
# =========================
def export_students_csv(students):
    if not students:
        print("\nNo Students Available to Export. ❌")
        return

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"reports/student_report_{timestamp}.csv"

    fields = [
        "student_id",
        "name",
        "email",
        "phone",
        "department",
        "semester",
        "CGPA",
        "total_marks",
        "maximum_marks",
        "percentage",
        "grade"
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fields,
            extrasaction="ignore"
        )

        writer.writeheader()

        for student in students:
            writer.writerow(student)

    print(f"\nStudent report exported successfully: {file_path} ✅")

# EXPORT STUDENTS TO EXCEL
# =========================
def export_students_excel(students):
    if not students:
        print("\nNo Students Available to Export. ❌")
        return

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"reports/student_report_{timestamp}.xlsx"

    fields = [
        "student_id",
        "name",
        "email",
        "phone",
        "department",
        "semester",
        "CGPA",
        "total_marks",
        "maximum_marks",
        "percentage",
        "grade"
    ]

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Students"

    sheet.append(fields)

    for student in students:
        row = []

        for field in fields:
            row.append(student.get(field, ""))

        sheet.append(row)

    workbook.save(file_path)

    print(f"\nStudent Excel report exported successfully: {file_path} ✅")

# ACADEMIC SUMMARY
# =========================
def get_academic_summary(students):

    total_students = len(students)

    # Safe float CGPA handling (defaults to 0.0 if CGPA is None)
    total_cgpa = sum(
        float(student.get("CGPA") or 0.0) for student in students
    )

    average_cgpa = (
        total_cgpa / total_students
        if total_students
        else 0
    )

    highest_cgpa = (
        max(students, key=lambda student: float(student.get("CGPA") or 0.0))
        if students
        else None
    )

    lowest_cgpa = (
        min(students, key=lambda student: float(student.get("CGPA") or 0.0))
        if students
        else None
    )

    department_counts = {}
    department_cgpa = {}

    semester_counts = {}
    semester_cgpa = {}

    students_with_results = []

    # STUDENT STATISTICS
    for student in students:
        cgpa_val = float(student.get("CGPA") or 0.0)

        # Department statistics
        department = student.get("department", "Unknown")

        department_counts[department] = (
            department_counts.get(department, 0) + 1
        )

        department_cgpa[department] = (
            department_cgpa.get(department, 0.0) + cgpa_val
        )

        # Semester statistics
        semester = student.get("semester", 1)

        semester_counts[semester] = (
            semester_counts.get(semester, 0) + 1
        )

        semester_cgpa[semester] = (
            semester_cgpa.get(semester, 0.0) + cgpa_val
        )

        # Result availability
        if student.get("percentage") is not None and student.get("grade") is not None:
            students_with_results.append(student)

    students_without_results = (
        total_students - len(students_with_results)
    )

    # AVERAGE PERCENTAGE
    if students_with_results:
        average_percentage = (
            sum(
                float(student["percentage"])
                for student in students_with_results
            )
            / len(students_with_results)
        )
    else:
        average_percentage = None

    # GRADE COUNTS
    grade_counts = {}
    for student in students_with_results:
        grade = student.get("grade", "N/A")
        grade_counts[grade] = (
            grade_counts.get(grade, 0) + 1
        )

    # SUBJECT ANALYTICS
    subject_marks = {}
    subject_counts = {}

    for student in students:
        for subject, marks in student.get("marks", {}).items():
            if marks is not None:
                subject_marks[subject] = (
                    subject_marks.get(subject, 0.0) + float(marks)
                )
                subject_counts[subject] = (
                    subject_counts.get(subject, 0) + 1
                )

    subject_averages = {}
    for subject in subject_marks:
        if subject_counts[subject] > 0:
            subject_averages[subject] = (
                subject_marks[subject] / subject_counts[subject]
            )

    # BEST AND WEAKEST SUBJECT
    highest_subject = None
    lowest_subject = None

    if subject_averages:
        highest_subject = max(
            subject_averages,
            key=subject_averages.get
        )
        lowest_subject = min(
            subject_averages,
            key=subject_averages.get
        )

    # STUDENT RANKING
    student_ranking = sorted(
        students_with_results,
        key=lambda student: float(student.get("percentage") or 0.0),
        reverse=True
    )

    return {
        "total_students": total_students,
        "total_cgpa": total_cgpa,
        "average_cgpa": average_cgpa,
        "highest_cgpa": highest_cgpa,
        "lowest_cgpa": lowest_cgpa,
        "department_counts": department_counts,
        "department_cgpa": department_cgpa,
        "semester_counts": semester_counts,
        "semester_cgpa": semester_cgpa,
        "subject_marks": subject_marks,
        "subject_counts": subject_counts,
        "subject_averages": subject_averages,
        "highest_subject": highest_subject,
        "lowest_subject": lowest_subject,
        "students_with_results": students_with_results,
        "student_ranking": student_ranking,
        "students_without_results": students_without_results,
        "average_percentage": average_percentage,
        "grade_counts": grade_counts
    }


# STUDENT PERFORMANCE REPORT
# =========================

def get_student_performance_report(student):

    percentage = student.get("percentage")

    if percentage is None:
        performance_level = "Result Not Available"
        status = "Result Not Available"

    elif percentage >= 85:
        performance_level = "Excellent"
        status = "Passed"

    elif percentage >= 70:
        performance_level = "Good"
        status = "Passed"

    elif percentage >= 50:
        performance_level = "Satisfactory"
        status = "Passed"

    else:
        performance_level = "Needs Improvement"
        status = "Failed"

    return {
    "student_id": student["student_id"],
    "name": student["name"],
    "department": student["department"],
    "semester": student["semester"],
    "CGPA": student["CGPA"],
    "marks": student.get("marks", {}),
    "total_marks": student.get("total_marks"),
    "maximum_marks": student.get("maximum_marks"),
    "percentage": percentage,
    "grade": student.get("grade"),
    "status": status,
    "performance_level": performance_level
}

# EXPORT STUDENT PERFORMANCE REPORT TO PDF
# =========================================
def export_student_performance_pdf(report):
    try:
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = f"reports/{report['student_id']}_performance_report_{timestamp}.pdf"

        document = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Student Performance Report", styles["Title"]))
        elements.append(Spacer(1, 15))

        elements.append(Paragraph(f"<b>Student ID:</b> {report['student_id']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Name:</b> {report['name']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Department:</b> {report['department']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Semester:</b> {report['semester']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>CGPA:</b> {report['CGPA']}", styles["Normal"]))

        elements.append(Spacer(1, 15))
        elements.append(Paragraph("Academic Result", styles["Heading2"]))

        if report["marks"]:
            for subject, marks in report["marks"].items():
                elements.append(Paragraph(f"{subject}: {marks}", styles["Normal"]))

            elements.append(Spacer(1, 10))
            elements.append(Paragraph(f"<b>Total Marks:</b> {report['total_marks']}/{report['maximum_marks']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Percentage:</b> {report['percentage']:.2f}%", styles["Normal"]))
            elements.append(Paragraph(f"<b>Grade:</b> {report['grade']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Status:</b> {report['status']}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Performance Level:</b> {report['performance_level']}", styles["Normal"]))
        else:
            elements.append(Paragraph("Academic Result: Not Available", styles["Normal"]))

        document.build(elements)
        print(f"\nStudent performance PDF exported successfully: {file_path} ✅")

    except Exception as e:
        print(f"\nError generating PDF: {e} ❌")


#export to excel
#=========================
def export_students_to_excel(students, filepath="reports/students_data.xlsx"):
    if not students:
        return None

    # Data formatting for Excel
    export_data = []
    for s in students:
        row = {
            "Student ID": s.get("student_id"),
            "Name": s.get("name"),
            "Email": s.get("email"),
            "Phone": s.get("phone"),
            "Department": s.get("department"),
            "Semester": s.get("semester"),
            "CGPA": s.get("CGPA"),
            "Percentage": s.get("percentage"),
            "Grade": s.get("grade"),
            "Marks JSON": json.dumps(s.get("marks", {}))
        }
        export_data.append(row)

    df = pd.DataFrame(export_data)
    df.to_excel(filepath, index=False)
    return filepath

#import to excel
#==============================
def import_students_from_excel(file_stream):
    # Reads uploaded Excel/CSV file into a DataFrame
    try:
        if file_stream.filename.endswith('.csv'):
            df = pd.read_csv(file_stream)
        else:
            df = pd.read_excel(file_stream)

        imported_students = []
        for _, row in df.iterrows():
            marks_raw = row.get("Marks JSON", "{}")
            if isinstance(marks_raw, str):
                try:
                    marks = json.loads(marks_raw)
                except:
                    marks = {}
            else:
                marks = {}

            student = {
                "student_id": str(row["Student ID"]),
                "name": str(row["Name"]),
                "email": str(row["Email"]),
                "phone": str(row["Phone"]),
                "department": str(row["Department"]),
                "semester": int(row["Semester"]),
                "CGPA": float(row["CGPA"]),
                "marks": marks
            }
            imported_students.append(student)

        return imported_students, None
    except Exception as e:
        return [], str(e)