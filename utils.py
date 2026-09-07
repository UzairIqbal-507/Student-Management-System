import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pandas as pd

# EMAIL CONFIGURATION (Set your SMTP details here or via environment variables)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "iqbaluzair507@gmail.com"  # Replace with sender email
SENDER_PASSWORD = "lncc mied cfdk jcsv"          # Replace with Gmail App Password

def send_result_email(student_email, student_name, student_id, pdf_path):
    """Sends an automated email notification with attached PDF report."""
    if SENDER_EMAIL == "your-school-email@gmail.com":
        print("[Email Alert] SMTP Credentials not configured. Skipping email send.")
        return False, "SMTP Credentials not set up in utils.py"

    try:
        msg = MIMEMultipart()
        msg['From'] = f"EduPulse Pro <{SENDER_EMAIL}>"
        msg['To'] = student_email
        msg['Subject'] = f"Academic Performance Report - {student_name} ({student_id})"

        body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <h2 style="color: #6366f1;">EduPulse Pro Academic Notification</h2>
                <p>Dear <strong>{student_name}</strong>,</p>
                <p>Your latest academic performance record and mark sheet have been updated on the student portal.</p>
                <p>Please find your official performance PDF report attached to this email.</p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <p style="font-size: 12px; color: #94a3b8;">This is an automated system notification. Please do not reply directly to this email.</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body_html, 'html'))

        # Attach PDF Report
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
                msg.attach(attach)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully!"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False, str(e)


def get_academic_summary(students):
    if not students:
        return {
            "total_students": 0,
            "average_cgpa": 0.0,
            "department_counts": {},
            "grade_counts": {},
            "subject_averages": {}
        }

    total_students = len(students)
    total_cgpa = sum(s.get("CGPA", 0.0) for s in students)
    avg_cgpa = round(total_cgpa / total_students, 2)

    dept_counts = {}
    grade_counts = {}
    subject_totals = {}
    subject_counts = {}

    for s in students:
        dept = s.get("department", "Unknown")
        dept_counts[dept] = dept_counts.get(dept, 0) + 1

        grade = s.get("grade", "N/A")
        grade_counts[grade] = grade_counts.get(grade, 0) + 1

        marks = s.get("marks", {})
        if isinstance(marks, dict):
            for sub, score in marks.items():
                subject_totals[sub] = subject_totals.get(sub, 0.0) + float(score)
                subject_counts[sub] = subject_counts.get(sub, 0) + 1

    subj_averages = {sub: round(subject_totals[sub] / subject_counts[sub], 2) for sub in subject_totals}

    return {
        "total_students": total_students,
        "average_cgpa": avg_cgpa,
        "department_counts": dept_counts,
        "grade_counts": grade_counts,
        "subject_averages": subj_averages
    }


def get_student_performance_report(student):
    marks = student.get("marks", {})
    return {
        "student_id": student.get("student_id"),
        "name": student.get("name"),
        "department": student.get("department"),
        "semester": student.get("semester"),
        "cgpa": student.get("CGPA"),
        "total_marks": student.get("total_marks"),
        "maximum_marks": student.get("maximum_marks"),
        "percentage": student.get("percentage"),
        "grade": student.get("grade"),
        "marks": marks
    }


def export_student_performance_pdf(report):
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    filepath = os.path.join(reports_dir, f"{report['student_id']}_report.pdf")
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor('#1e293b'), alignment=1)
    subtitle_style = ParagraphStyle('SubTitle', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.HexColor('#64748b'), alignment=1)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor('#0f172a'))
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#334155'))

    elements = []
    elements.append(Paragraph("<b>EDUPULSE PRO ACADEMIC REPORT</b>", title_style))
    elements.append(Paragraph("Institutional Student Performance Evaluation", subtitle_style))
    elements.append(Spacer(1, 15))

    info_data = [
        [Paragraph(f"<b>Student Name:</b> {report['name']}", normal_style), Paragraph(f"<b>Student ID:</b> {report['student_id']}", normal_style)],
        [Paragraph(f"<b>Department:</b> {report['department']}", normal_style), Paragraph(f"<b>Semester:</b> {report['semester']}", normal_style)],
        [Paragraph(f"<b>Cumulative GPA:</b> {report['cgpa']:.2f}", normal_style), Paragraph(f"<b>Overall Grade:</b> {report['grade']}", normal_style)]
    ]
    info_table = Table(info_data, colWidths=[270, 270])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Subject Wise Breakdown</b>", heading_style))
    elements.append(Spacer(1, 8))

    marks_data = [["Subject", "Marks Obtained", "Total Marks", "Status"]]
    for sub, score in report.get("marks", {}).items():
        status = "Passed" if float(score) >= 50 else "Needs Improvement"
        marks_data.append([sub, str(score), "100", status])

    marks_table = Table(marks_data, colWidths=[180, 120, 120, 120])
    marks_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(marks_table)
    elements.append(Spacer(1, 15))

    pct_str = f"{report['percentage']:.2f}%" if report.get("percentage") else "N/A"
    summary_data = [
        ["Total Marks Obtained", f"{report['total_marks']} / {report['maximum_marks']}"],
        ["Overall Percentage", pct_str]
    ]
    summary_table = Table(summary_data, colWidths=[270, 270])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    elements.append(summary_table)

    doc.build(elements)
    return filepath


def export_students_to_excel(students):
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    filepath = os.path.join(reports_dir, "Students_Export.xlsx")
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
            "Total Marks": s.get("total_marks"),
            "Percentage": s.get("percentage"),
            "Grade": s.get("grade")
        }
        for sub, val in s.get("marks", {}).items():
            row[f"Marks_{sub}"] = val

        export_data.append(row)

    df = pd.DataFrame(export_data)
    df.to_excel(filepath, index=False)
    return filepath


def import_students_from_excel(file_storage):
    try:
        filename = file_storage.filename
        if filename.endswith('.csv'):
            df = pd.read_csv(file_storage)
        else:
            df = pd.read_excel(file_storage)

        imported = []
        for _, row in df.iterrows():
            student_id = str(row.get("Student ID", "")).strip()
            name = str(row.get("Name", "")).strip()
            email = str(row.get("Email", "")).strip()
            phone = str(row.get("Phone", "")).strip()
            department = str(row.get("Department", "")).strip()
            semester = int(row.get("Semester", 1))
            cgpa = float(row.get("CGPA", 0.0))

            marks = {}
            for col in df.columns:
                if col.startswith("Marks_"):
                    sub_name = col.replace("Marks_", "")
                    val = row.get(col, 0)
                    marks[sub_name] = float(val) if pd.notnull(val) else 0.0

            if student_id and name and email:
                imported.append({
                    "student_id": student_id,
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "semester": semester,
                    "CGPA": cgpa,
                    "marks": marks
                })

        return imported, None
    except Exception as e:
        return [], str(e)