# 🎓 EduPulse Pro — Advanced Student Management System

**EduPulse Pro** is a enterprise-grade, web-based Student Management & Academic Analytics System built with **Flask (Python)**, **PostgreSQL**, and **Bootstrap 5**. It features Role-Based Access Control (RBAC), dynamic academic department/subject management, automated PDF report generation, email notifications, bulk data processing, and real-time analytical dashboards.

---

## 🔥 Key Features

### 🔐 1. Multi-Role Authentication & Access Control (RBAC)
* **Admin Portal**: Full access to student records, dynamic subject setup, bulk operations, analytical dashboards, and system audit logs.
* **Student Portal**: Restricted self-service portal where students can only view their own marks, performance summary, and download/email their marksheets.
* **Security & Encryption**: Password hashing using `Werkzeug` security standards and protected session routing.

### 🏢 2. Dynamic Department & Subject Management
* **Custom Departments**: Admins can dynamically create and manage departments (e.g., Data Science, AI, Cyber Security).
* **Subject Mapping**: Assign customized course structures to specific departments.
* **Dynamic Forms**: Student registration forms dynamically render subject input fields based on the chosen department.

### 📊 3. Interactive Analytics & Performance Metrics
* **Visual Charts**: Integrated **Chart.js** visualizations for department breakdown, grade distributions, and subject performance averages.
* **Real-Time Search & Sorting**: Instant client-side filtering and natural numeric Student ID sorting (`STU-1`, `STU-2`, ... `STU-10`).
* **Automated Calculations**: Dynamic GPA, total marks, percentage, and letter grade evaluations (`A+` to `F`).

### 📧 4. Automated Reporting & PDF Mailer
* **PDF Marksheet Generation**: Instant PDF report card generation using `ReportLab`.
* **Automated Email Notifications**: One-click emailing of official PDF report cards directly to student email addresses via SMTP.

### 📁 5. Data Science & Bulk Operations
* **Excel/CSV Bulk Import**: Upload multi-student datasets directly into PostgreSQL with automated validation and error handling.
* **Excel Data Export**: Export student records and marks breakdown to structured `.xlsx` files with a single click.

### 🛡️ 6. System Audit Logs & Account Settings
* **Activity Tracking**: Tracks user logins, record additions, updates, deletions, and data exports.
* **User Profile & Security**: In-app password change mechanism with current password verification.

---

## 🛠️ Tech Stack & Dependencies

* **Backend Framework:** Python 3.12+ / Flask
* **Database Management:** PostgreSQL (via `psycopg2-binary`)
* **Frontend UI:** HTML5, Bootstrap 5.3 (Dark Glassmorphism Theme), FontAwesome 6, Chart.js
* **Reporting & Mailer:** ReportLab (PDF), Python SMTP (`smtplib`, `email`)
* **Data Processing:** Pandas, OpenPyXL
* **Security:** Werkzeug Password Hashing

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
Ensure you have the following installed on your machine:
* Python 3.10 or higher
* PostgreSQL Database Server

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/student-management-system.git](https://github.com/your-username/student-management-system.git)
cd student-management-system