# 🎓 EduPulse Pro — Student Management System

A high-performance, commercial-grade Student Management Web Application built with Python (Flask), PostgreSQL, and a modern Glassmorphism Dark UI/UX.

---

## 🚀 Key Features

- 🔐 **Authentication & RBAC**: Secure role-based user login (Admin vs. Student) with hashed passwords using `werkzeug.security`.
- 🗄️ **PostgreSQL Backend**: Relational database storage with native `JSONB` support for dynamic marks, relational tables, and CASCADE rules.
- 📚 **Dynamic Departmental Subjects**: Tailored subject fields based on department (Data Science, Computer Science, SE, IT).
- 📊 **Visual Analytics Dashboard**: Interactive visual insights powered by `Chart.js` (Department Distribution, Grade Ranges, Subject Averages).
- 📥 **Bulk Import & Export**: One-click Excel (.xlsx) / CSV directory export and bulk student onboarding via file upload (`pandas` + `openpyxl`).
- 📄 **PDF Report Generation**: Institutional PDF performance reports generated on the fly (`ReportLab`).
- 📜 **Audit Trail & System Logs**: Complete tracking of critical operations (Add, Edit, Delete, Bulk Upload) with timestamps.
- 🎨 **Glassmorphic UI/UX**: Dark mode layout with instant client-side search, SweetAlert2 popups, and active button loading states.

---

## 🛠️ Tech Stack & Dependencies

- **Backend**: Python, Flask
- **Database**: PostgreSQL (`psycopg2`)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, FontAwesome 6, Chart.js, SweetAlert2
- **Data & File Processing**: Pandas, OpenPyXL, ReportLab, Werkzeug

---

## 📂 Project Architecture

```text
Student Management System/
│
├── app.py                   # Main Flask routes & middleware
├── database.py              # PostgreSQL queries & schema initialization
├── utils.py                 # PDF generation, Analytics summary, Excel import/export
├── validation.py            # Input validation & grading calculations
├── migrate.py               # JSON to PostgreSQL migration utility
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
│
├── static/                  # Static assets & custom styling
├── templates/               # HTML Templates
│   ├── layout.html          # Base Glassmorphism layout
│   ├── index.html           # Main student directory & instant filter
│   ├── dashboard.html       # Chart.js analytics view
│   ├── add.html             # Dynamic student creation form
│   ├── update.html          # Student details editor
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   └── logs.html            # Audit trail log view
└── reports/                 # Output directory for generated PDF & Excel files