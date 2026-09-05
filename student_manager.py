from validation import (get_non_empty_input, get_semester,
                        get_department, get_cgpa,
                        get_email, get_phone, get_name,
                        get_student_id, get_search_choice,
                        get_marks, calculate_result,
                        get_percentage_range, get_semester_range,
                        get_cgpa_range, get_sort_order, get_backup_choice)

from utils import (get_backups, restore_students, backup_students,
                   export_students_csv, export_students_excel,
                   get_academic_summary, get_student_performance_report,
                   export_student_performance_pdf)

from database import (db_get_all_students, db_get_student_by_id,
                      db_add_student, db_update_student, db_delete_student)


# GET MARKS FOR SUBJECT
# ========================
def get_subject_marks(department):
    subject_mapping = {
        "Data Science": ["Python", "Statistics", "Machine Learning", "Linear Algebra"],
        "Computer Science": ["Programming Fundamentals", "Data Structures", "DBMS", "OS"],
        "Software Engineering": ["Software Design", "SQA", "Web Engineering", "DBMS"],
        "Information Technology": ["Networking", "Cyber Security", "Web Tech", "Cloud Computing"]
    }

    subjects = subject_mapping.get(department, ["Subject 1", "Subject 2", "Subject 3", "Subject 4"])
    marks = {}
    for subject in subjects:
        marks[subject] = get_marks(subject)
    return marks


# ADD STUDENTS
# ==================
def add_students():
    print("\n===== Add students ======")

    students = db_get_all_students()
    student_id = get_student_id()

    # Check duplicate ID
    for student in students:
        if student["student_id"] == student_id:
            print("STUDENT ALREADY EXIST !!...☠️")
            return

    name = get_name()
    email = get_email()

    # Check duplicate email and phone
    for student in students:
        if student["email"].lower() == email.lower():
            print("EMAIL ALREADY EXISTS !!...❌")
            return

    phone = get_phone()
    for student in students:
        if student["phone"] == phone:
            print("PHONE NUMBER ALREADY EXISTS !!...❌")
            return

    department = get_department()
    semester = get_semester()
    cgpa = get_cgpa()
    marks = get_subject_marks(department)
    total_marks, maximum_marks, percentage, grade = calculate_result(marks)

    student = {
        "student_id": student_id,
        "name": name,
        "email": email,
        "phone": phone,
        "department": department,
        "semester": semester,
        "CGPA": cgpa,
        "marks": marks,
        "total_marks": total_marks,
        "maximum_marks": maximum_marks,
        "percentage": percentage,
        "grade": grade
    }

    db_add_student(student)
    print("\n===== Student added successfully! ✅ ======")


# VIEW STUDENTS
# =====================
def view_students():
    students = db_get_all_students()
    if not students:
        print("\nSTUDENT NOT FOUND!!!")
        return

    print("\n========== Students ===========")
    for student in students:
        print(f'id : {student["student_id"]}')
        print(f'name: {student["name"]}')
        print(f'email: {student["email"]}')
        print(f'phone: {student["phone"]}')
        print(f'department: {student["department"]}')
        print(f'semester: {student["semester"]}')
        print(f'cgpa: {student["CGPA"]}')

        if "marks" in student and student["marks"]:
            print("----- Academic Result -----")
            for subject, marks in student["marks"].items():
                print(f'{subject}: {marks}')

            print(f'Total Marks: {student["total_marks"]}/{student["maximum_marks"]}')
            perc = student.get("percentage")
            print(f'Percentage: {perc:.2f}%' if perc is not None else 'Percentage: N/A')
            print(f'Grade: {student["grade"]}')

        else:
            print("Academic Result: Not Available...❌")

        print('--------------------------------------------')


# SEARCH STUDENTS
# ====================
def search_students():
    students = db_get_all_students()
    if not students:
        print("\nSTUDENT NOT FOUND!!!❌")
        return

    print("\n========== SEARCH STUDENTS ===========")
    print("1. SEARCH BY ID.... ")
    print("2. SEARCH BY NAME... ")
    print("3. SEARCH BY DEPARTMENT... ")
    print("4. SEARCH BY SEMESTER... ")
    print("5. SEARCH BY CGPA... ")
    print("6. SEARCH BY PERCENTAGE....")
    print("7. SEARCH BY SEMESTER RANGE...")

    choice = get_search_choice()

    if choice == "1":
        student_id = get_student_id()
        student = db_get_student_by_id(student_id)
        if student:
            display_student(student)
        else:
            print("\nStudent not found❌")

    elif choice == "2":
        name = input("Enter student name: ").strip().lower()
        matching_students = [s for s in students if name in s["name"].lower()]
        display_students_list(matching_students)

    elif choice == "3":
        department = get_department()
        matching_students = [s for s in students if s["department"] == department]
        display_students_list(matching_students)

    elif choice == "4":
        print("\nSelect Semester:")
        semester = get_semester()
        matching_students = [s for s in students if s["semester"] == semester]
        display_students_list(matching_students)

    elif choice == "5":
        print("\nSelect CGPA Range:")
        minimum, maximum = get_cgpa_range()
        matching_students = [s for s in students if minimum <= s["CGPA"] <= maximum]
        display_students_list(matching_students)

    elif choice == "6":
        minimum, maximum = get_percentage_range()
        matching_students = [s for s in students if s.get("percentage") is not None and minimum <= s["percentage"] <= maximum]
        display_students_list(matching_students)

    elif choice == "7":
        minimum, maximum = get_semester_range()
        matching_students = [s for s in students if minimum <= s["semester"] <= maximum]
        display_students_list(matching_students)

    else:
        print("\nInvalid Search Choice!!❌")


# DISPLAY ONE STUDENT
# ========================
def display_student(student):
    print("\n========== STUDENT ==========")
    print(f"ID: {student['student_id']}")
    print(f"Name: {student['name']}")
    print(f"Email: {student['email']}")
    print(f"Phone: {student['phone']}")
    print(f"Department: {student['department']}")
    print(f"Semester: {student['semester']}")
    print(f"CGPA: {student['CGPA']}")

    if "marks" in student and student["marks"]:
        print("----- Academic Result -----")
        for subject, marks in student["marks"].items():
            print(f"{subject}: {marks}")

        print(f"Total Marks: {student['total_marks']}/{student['maximum_marks']}")
        perc = student.get("percentage")
        print(f"Percentage: {perc:.2f}%" if perc is not None else "Percentage: N/A")
        print(f"Grade: {student['grade']}")
    else:
        print("Academic Result: Not Available....❌")


# DISPLAY STUDENTS LIST
# ===========================
def display_students_list(students):
    if not students:
        print("\nSTUDENT NOT FOUND!!!❌")
        return

    for student in students:
        display_student(student)

    print(f"\nTotal Students Found: {len(students)}")


# DELETE STUDENTS
# ====================
def delete_students():
    student_id = input("Enter student id: ").strip()
    student = db_get_student_by_id(student_id)

    if student:
        print("Student Found : ")
        display_student(student)

        confirm = input("Do you want to delete student ? (y/n): ").lower()
        if confirm == "y":
            db_delete_student(student_id)
            print("Student Deleted Successfully!👏")
        else:
            print("\nDelete Cancelled.")
    else:
        print('\nStudent Not Found!!')


# STATISTICS
# ===============
def statistics():
    students = db_get_all_students()
    if not students:
        print("\nNo Students Available.")
        return

    summary = get_academic_summary(students)

    total_students = summary["total_students"]
    total_cgpa = summary["total_cgpa"]
    average_cgpa = summary["average_cgpa"]
    highest_cgpa = summary["highest_cgpa"]
    lowest_cgpa = summary["lowest_cgpa"]

    department_counts = summary["department_counts"]
    department_cgpa = summary["department_cgpa"]

    semester_counts = summary["semester_counts"]

    students_with_results = summary["students_with_results"]
    students_without_results = summary["students_without_results"]
    average_percentage = summary["average_percentage"]
    grade_counts = summary["grade_counts"]

    print("\n============= STATISTICS =============")
    print(f"Total Students: {total_students}")
    print(f"Total CGPA: {total_cgpa}")
    print(f"Average CGPA: {average_cgpa:.2f}")

    print(f"Highest CGPA: {highest_cgpa['CGPA']}   {highest_cgpa['name']}")
    print(f"Lowest CGPA: {lowest_cgpa['CGPA']}   {lowest_cgpa['name']}")

    print("\n----------- Department Distribution -----------")
    for department, count in sorted(department_counts.items()):
        print(f"{department}: {count} student(s)")

    print("\n----------- Department Performance -----------")
    for department, count in sorted(department_counts.items()):
        avg_dept_cgpa = department_cgpa[department] / count
        print(f"{department}: {avg_dept_cgpa:.2f} average CGPA")

    print("\n----------- Semester Distribution -----------")
    for semester, count in sorted(semester_counts.items()):
        print(f"Semester {semester}: {count} student(s)")

    print("\n----------- Academic Result Availability -----------")
    print(f"Students with results: {len(students_with_results)}")
    print(f"Students without results: {students_without_results}")

    if average_percentage is not None:
        print(f"\nAverage Percentage: {average_percentage:.2f}%")
        print("------- Grade Distribution -------")
        for grade, count in sorted(grade_counts.items()):
            print(f"{grade}: {count} student(s)")
    else:
        print("\nAverage Percentage: Not Available")
        print("Grade Distribution: Not Available")


# STUDENT DASHBOARD
# =========================
def dashboard():
    students = db_get_all_students()
    if not students:
        print("\nNo Students Available.")
        return

    summary = get_academic_summary(students)

    total_students = summary["total_students"]
    average_cgpa = summary["average_cgpa"]

    highest_cgpa = summary["highest_cgpa"]
    lowest_cgpa = summary["lowest_cgpa"]

    students_with_results = summary["students_with_results"]
    students_without_results = summary["students_without_results"]
    grade_counts = summary["grade_counts"]
    department_counts = summary["department_counts"]
    department_cgpa = summary["department_cgpa"]
    semester_counts = summary["semester_counts"]
    semester_cgpa = summary["semester_cgpa"]
    subject_averages = summary["subject_averages"]
    highest_subject = summary["highest_subject"]
    lowest_subject = summary["lowest_subject"]
    student_ranking = summary["student_ranking"]

    passed_students = [s for s in students_with_results if s["percentage"] >= 50]
    failed_students = [s for s in students_with_results if s["percentage"] < 50]
    pass_rate = (len(passed_students) / len(students_with_results)) * 100 if students_with_results else None

    top_performers = sorted(students_with_results, key=lambda s: s["percentage"], reverse=True)[:3]

    best_department = max(
        department_cgpa,
        key=lambda dept: department_cgpa[dept] / department_counts[dept]
    )
    best_department_cgpa = department_cgpa[best_department] / department_counts[best_department]

    best_semester = max(
        semester_cgpa,
        key=lambda sem: semester_cgpa[sem] / semester_counts[sem]
    )
    best_semester_cgpa = semester_cgpa[best_semester] / semester_counts[best_semester]

    at_risk_students = [s for s in students_with_results if s["percentage"] < 70]

    print("\n╔════════════════════════════════════════╗")
    print("║        STUDENT MANAGEMENT DASHBOARD    ║")
    print("╠════════════════════════════════════════╣")
    print(f"║ Total Students     : {total_students:<15}║")
    print(f"║ Average CGPA       : {average_cgpa:<15.2f}║")
    print(f"║ Highest CGPA       : {highest_cgpa['CGPA']:<15}║")
    print(f"║ Lowest CGPA        : {lowest_cgpa['CGPA']:<15}║")
    print("╠════════════════════════════════════════╣")
    print("║ Departments                             ║")

    for department, count in sorted(department_counts.items()):
        print(f"║ {department:<20}: {count:<12}║")

    print("╠════════════════════════════════════════╗")
    print("║ Performance Leaders                    ║")
    print(f"║ Best Department : {best_department:<15}║")
    print(f"║ Average CGPA    : {best_department_cgpa:<15.2f}║")
    print(f"║ Best Semester   : Semester {best_semester:<7}║")
    print(f"║ Average CGPA    : {best_semester_cgpa:<15.2f}║")

    print("╠════════════════════════════════════════╣")
    print("║ Department Performance                 ║")
    for department, count in sorted(department_counts.items()):
        avg_dept_cgpa = department_cgpa[department] / count
        print(f"║ {department:<20}: {avg_dept_cgpa:.2f} CGPA   ║")

    print("║ Semesters                               ║")
    for semester, count in sorted(semester_counts.items()):
        print(f"║ Semester {semester:<11}: {count:<12}║")

    print("╠════════════════════════════════════════╗")
    print("║ Semester Performance                  ║")
    for semester, count in sorted(semester_counts.items()):
        avg_sem_cgpa = semester_cgpa[semester] / count
        print(f"║ Semester {semester:<11}: {avg_sem_cgpa:.2f} CGPA   ║")

    print("╠════════════════════════════════════════╗")
    print("║ Subject Performance                    ║")
    for subject, average in sorted(subject_averages.items()):
        print(f"║ {subject:<20}: {average:.2f} average marks ║")

    print("╠════════════════════════════════════════╗")
    print("║ Subject Insights                       ║")
    if highest_subject:
        print(f"║ Best Subject    : {highest_subject:<20}║")
        print(f"║ Average Marks   : {subject_averages[highest_subject]:.2f}             ║")

    if lowest_subject:
        print(f"║ Weakest Subject : {lowest_subject:<20}║")
        print(f"║ Average Marks   : {subject_averages[lowest_subject]:.2f}             ║")

    print("╠════════════════════════════════════════╣")
    print("║ Results Overview                       ║")
    print(f"║ Results Available : {len(students_with_results):<15}║")
    print(f"║ Results Missing   : {students_without_results:<15}║")

    print("╠════════════════════════════════════════╣")
    print("║ Result Status                          ║")
    print(f"║ Passed           : {len(passed_students):<18}║")
    print(f"║ Failed           : {len(failed_students):<18}║")
    print(f"║ Missing          : {students_without_results:<18}║")
    if pass_rate is not None:
        print(f"║ Pass Rate        : {pass_rate:<17.2f}%║")
    else:
        print("║ Pass Rate        : Not Available     ║")

    print("╠════════════════════════════════════════╣")
    average_percentage = summary["average_percentage"]
    print("║ Academic Insight                       ║")
    print(f"║ Average CGPA       : {average_cgpa:<14.2f}║")

    if average_percentage is not None:
        print(f"║ Average Percentage : {average_percentage:<14.2f}%║")
    else:
        print("║ Average Percentage : Not Available    ║")

    print("╠════════════════════════════════════════╣")
    print("║ Top Performers                         ║")
    if top_performers:
        for index, student in enumerate(top_performers, start=1):
            print(
                f"║ {index}. {student['name']:<12} "
                f"{student['percentage']:.2f}%  "
                f"CGPA: {student['CGPA']:.2f}  "
                f"{student['grade']:<3} ║"
            )
    else:
        print("║ No Results Available                  ║")

    print("╠════════════════════════════════════════╣")
    print("║ Grade Distribution                     ║")
    if grade_counts:
        for grade, count in sorted(grade_counts.items()):
            print(f"║ Grade {grade:<10}: {count:<15}║")
    else:
        print("║ No Grades Available                   ║")

    excellent = sum(1 for s in students_with_results if s["percentage"] >= 85)
    good = sum(1 for s in students_with_results if 70 <= s["percentage"] < 85)
    needs_improvement = sum(1 for s in students_with_results if s["percentage"] < 70)

    print("╠════════════════════════════════════════╗")
    print("║ At-Risk Students                       ║")

    if at_risk_students:
        for student in at_risk_students:
            print(
                f"║ {student['name']:<15} "
                f"{student['percentage']:.2f}% "
                f"({student['grade']})              ║"
            )
    else:
        print("║ No At-Risk Students 🎉                 ║")

    print("╠════════════════════════════════════════╣")
    print("║ Performance Summary                    ║")
    print(f"║ Excellent (85%+) : {excellent:<18}║")
    print(f"║ Good (70-84%)    : {good:<18}║")
    print(f"║ Needs Improvement: {needs_improvement:<18}║")

    print("╠════════════════════════════════════════╗")
    print("║ Top Students                           ║")
    for rank, student in enumerate(student_ranking[:5], start=1):
        print(
            f"║ {rank}. {student['name']:<18} "
            f"{student.get('percentage', 0):>6.2f}% ║"
        )
    print("╚════════════════════════════════════════╝")


# EXPORT STUDENT REPORT
# =========================
def export_student_report():
    students = db_get_all_students()
    if not students:
        print("\nNo Students Available to Export. ❌")
        return

    print("\n========== EXPORT STUDENT REPORT ==========")
    print("1. Export as CSV")
    print("2. Export as Excel")
    print("3. Back")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        export_students_csv(students)
    elif choice == "2":
        export_students_excel(students)
    elif choice == "3":
        return
    else:
        print("\nInvalid export choice! ❌")


# UPDATE STUDENTS
# ==================
def update_students():
    student_id = get_student_id()
    student = db_get_student_by_id(student_id)

    if not student:
        print('\nStudent Not Found!!')
        return

    students = db_get_all_students()
    print("\nSTUDENT FOUND....✅")
    print("ENTER NEW INFORMATION.....")

    name = get_name()
    department = get_department()
    email = get_email()

    for other_student in students:
        if other_student["student_id"] != student_id:
            if other_student["email"].lower() == email.lower():
                print("EMAIL ALREADY EXISTS !!...❌")
                return

    phone = get_phone()
    for other_student in students:
        if other_student["student_id"] != student_id:
            if other_student["phone"] == phone:
                print("PHONE NUMBER ALREADY EXISTS !!...❌")
                return

    semester = get_semester()
    cgpa = get_cgpa()
    marks = get_subject_marks(department)
    total_marks, maximum_marks, percentage, grade = calculate_result(marks)

    updated_student = {
        "student_id": student_id,
        "name": name,
        "department": department,
        "email": email,
        "phone": phone,
        "semester": semester,
        "CGPA": cgpa,
        "marks": marks,
        "total_marks": total_marks,
        "maximum_marks": maximum_marks,
        "percentage": percentage,
        "grade": grade
    }

    db_update_student(updated_student)
    print("STUDENT UPDATED SUCCESSFULLY !! ✅")


# SORT STUDENTS BY CGPA
# ==========================
def sort_by_cgpa(students, order):
    if not students:
        print("\nNo Students Available.")
        return

    reverse = True if order == "1" else False
    sorted_students = sorted(students, key=lambda s: s["CGPA"], reverse=reverse)

    print("\n========= STUDENTS BY CGPA =========")
    for student in sorted_students:
        print(f"{student['name']} -> {student['CGPA']} CGPA")


# SORTING BY NAME
# ======================
def sort_by_name(students, order):
    if not students:
        print("\nNo Students Available.")
        return

    reverse = False if order == "1" else True
    sorted_students = sorted(students, key=lambda s: s["name"].lower(), reverse=reverse)

    print("\n========= STUDENTS BY NAME =========")
    for student in sorted_students:
        print(f"{student['name']} -> {student['CGPA']} CGPA")


# SORTING BY SEMESTER
# ========================
def sort_by_semester(students, order):
    if not students:
        print("\nNo Students Available.")
        return

    reverse = True if order == "1" else False
    sorted_students = sorted(students, key=lambda s: s["semester"], reverse=reverse)

    print("\n========= STUDENTS BY SEMESTER =========")
    for student in sorted_students:
        print(f"{student['name']} -> Semester {student['semester']}")


# SORTING BY PERCENTAGE
# =============================
def sort_by_percentage(students, order):
    students_with_results = [s for s in students if s.get("percentage") is not None]

    if not students_with_results:
        print("\nNo Student Results Available.")
        return

    reverse = True if order == "1" else False
    sorted_students = sorted(students_with_results, key=lambda s: s["percentage"], reverse=reverse)

    print("\n========= STUDENTS BY PERCENTAGE =========")
    for student in sorted_students:
        print(f"{student['name']} -> {student['percentage']:.2f}% ({student['grade']})")


# SORTING STUDENTS
# =====================
def sort_students():
    students = db_get_all_students()
    if not students:
        print("\nNo Students Available.")
        return

    print("\n========== SORT STUDENTS ==========")
    print("1. Sort by CGPA")
    print("2. Sort by Name")
    print("3. Sort by Semester")
    print("4. Sort by Percentage")

    choice = input("Enter your choice: ").strip()

    if choice in ["1", "2", "3", "4"]:
        order = get_sort_order()

        if choice == "1":
            sort_by_cgpa(students, order)
        elif choice == "2":
            sort_by_name(students, order)
        elif choice == "3":
            sort_by_semester(students, order)
        elif choice == "4":
            sort_by_percentage(students, order)
    else:
        print("\nInvalid sorting choice! ❌")


# RESTORE STUDENT DATA
# =========================
def restore_student_data():
    backups = get_backups()

    if not backups:
        print("\nNo Backups Available. ❌")
        return

    print("\n========== AVAILABLE BACKUPS ==========")
    for index, backup in enumerate(backups, start=1):
        print(f"{index}. {backup}")

    choice = get_backup_choice(backups)
    selected_backup = backups[choice]

    print(f"\nSelected Backup: {selected_backup}")

    confirmation = input("Are you sure you want to restore this backup? (y/n): ").strip().lower()

    if confirmation == "y":
        restore_students(selected_backup)
        print("\nReloading restored students data... 🔄")
    else:
        print("\nRestore Cancelled. ❌")


# STUDENT PERFORMANCE REPORT
# =========================
def student_performance_report():
    students = db_get_all_students()
    if not students:
        print("\nNo Students Available.")
        return

    student_id = get_student_id()
    student = db_get_student_by_id(student_id)

    if student:
        report = get_student_performance_report(student)

        print("\n╔════════════════════════════════════════╗")
        print("║       STUDENT PERFORMANCE REPORT       ║")
        print("╠════════════════════════════════════════╣")

        print(f"║ ID         : {report['student_id']:<23}║")
        print(f"║ Name       : {report['name']:<23}║")
        print(f"║ Department : {report['department']:<23}║")
        print(f"║ Semester   : {report['semester']:<23}║")
        print(f"║ CGPA       : {report['CGPA']:<23}║")

        print("╠════════════════════════════════════════╣")
        print("║ Academic Result                        ║")

        if report.get("marks"):
            for subject, marks in report["marks"].items():
                print(f"║ {subject:<15}: {marks:<15}║")

            print(f"║ Total Marks: {report['total_marks']}/{report['maximum_marks']:<10}║")
            print(f"║ Percentage : {report['percentage']:<15.2f}%║")
            print(f"║ Grade      : {report['grade']:<23}║")
            print(f"║ Status     : {report['status']:<23}║")
            print(f"║ Performance: {report['performance_level']:<23}║")
        else:
            print("║ Academic Result: Not Available         ║")

        print("╚════════════════════════════════════════╝")

        print("\n1. Export Report as PDF")
        print("2. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            export_student_performance_pdf(report)
        elif choice == "2":
            return
        else:
            print("\nInvalid choice! ❌")
        return

    print("\nStudent Not Found! ❌")