import json
import os
import csv
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

    total_cgpa = sum(
        student["CGPA"] for student in students
    )

    average_cgpa = (
        total_cgpa / total_students
        if total_students
        else 0
    )

    highest_cgpa = (
        max(students, key=lambda student: student["CGPA"])
        if students
        else None
    )

    lowest_cgpa = (
        min(students, key=lambda student: student["CGPA"])
        if students
        else None
    )

    department_counts = {}
    department_cgpa = {}

    semester_counts = {}
    semester_cgpa = {}

    students_with_results = []

    for student in students:

        # Department statistics
        department = student["department"]

        department_counts[department] = (
            department_counts.get(department, 0) + 1
        )

        department_cgpa[department] = (
            department_cgpa.get(department, 0)
            + student["CGPA"]
        )

        # Semester statistics
        semester = student["semester"]

        semester_counts[semester] = (
            semester_counts.get(semester, 0) + 1
        )

        semester_cgpa[semester] = (
            semester_cgpa.get(semester, 0)
            + student["CGPA"]
        )

        # Result availability
        if "percentage" in student and "grade" in student:
            students_with_results.append(student)

    students_without_results = (
        total_students - len(students_with_results)
    )

    if students_with_results:

        average_percentage = (
            sum(
                student["percentage"]
                for student in students_with_results
            )
            / len(students_with_results)
        )

    else:
        average_percentage = None

    grade_counts = {}

    for student in students_with_results:

        grade = student["grade"]

        grade_counts[grade] = (
            grade_counts.get(grade, 0) + 1
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
        "students_with_results": students_with_results,
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

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"reports/{report['student_id']}_performance_report_{timestamp}.pdf"

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "Student Performance Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            f"<b>Student ID:</b> {report['student_id']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Name:</b> {report['name']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Department:</b> {report['department']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Semester:</b> {report['semester']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>CGPA:</b> {report['CGPA']}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "Academic Result",
            styles["Heading2"]
        )
    )

    if report["marks"]:

        for subject, marks in report["marks"].items():
            elements.append(
                Paragraph(
                    f"{subject}: {marks}",
                    styles["Normal"]
                )
            )

        elements.append(Spacer(1, 10))

        elements.append(
            Paragraph(
                f"<b>Total Marks:</b> "
                f"{report['total_marks']}/{report['maximum_marks']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Percentage:</b> "
                f"{report['percentage']:.2f}%",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Grade:</b> {report['grade']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Status:</b> {report['status']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Performance Level:</b> "
                f"{report['performance_level']}",
                styles["Normal"]
            )
        )

    else:

        elements.append(
            Paragraph(
                "Academic Result: Not Available",
                styles["Normal"]
            )
        )

    document.build(elements)

    print(
        f"\nStudent performance PDF exported successfully: "
        f"{file_path} ✅"
    )