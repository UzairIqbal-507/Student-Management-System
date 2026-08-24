from validation import (get_non_empty_input, get_semester,
                        get_department, get_cgpa,
                        get_email, get_phone, get_name,
                        get_student_id, get_search_choice,
                        get_marks, calculate_result,
                        get_percentage_range,get_semester_range,
                        get_cgpa_range)

from utils import save_students

#ADD STUDENTS
#==================
def add_students(students):

    print ("\n=====Add students======")

    student_id = get_student_id()

    #Check duplicate ID in it
    for student in students:
        if student["student_id"] == student_id:
            print ("STUDENT ALREADY EXIST !!...☠️")
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
    marks=get_subject_marks()
    total_marks,maximum_marks,percentage,grade = calculate_result(marks)

    student={
        "student_id":student_id,
        "name":name,
        "email":email,
        "phone":phone,
        "department":department,
        "semester": semester,
        "CGPA": cgpa,
        "marks": marks,
        "total_marks": total_marks,
        "maximum_marks": maximum_marks,
        "percentage": percentage,
        "grade": grade
    }
    students.append(student)

    save_students(students)

    print ("\n=====Student added successfully!======")

#VIEW STUDENTS
#=====================
def view_students(students):
    if not students:
        print ("STUDENT NOT FOUND!!!")
        return

    print ("\n==========Students===========")
    for student in students:
        print(f'id : {student["student_id"]}')
        print(f'name: {student["name"]}')
        print(f'email: {student["email"]}')
        print(f'phone: {student["phone"]}')
        print(f'department: {student["department"]}')
        print(f'semester: {student["semester"]}')
        print(f'cgpa: {student["CGPA"]}')
        print(f'cgpa: {student["CGPA"]}')

        if "marks" in student:
            print("----- Academic Result -----")

            for subject, marks in student["marks"].items():
                print(f'{subject}: {marks}')

            print(f'Total Marks: {student["total_marks"]}/{student["maximum_marks"]}')
            print(f'Percentage: {student["percentage"]:.2f}%')
            print(f'Grade: {student["grade"]}')

        else:
            print("Academic Result: Not Available...❌")

        print(f'--------------------------------------------')


#SEARCH STUDENTS
#====================
def search_students(students):

    if not students:
        print ("\nSTUDENT NOT FOUND!!!❌")
        return

    print ("\n==========SEARCH STUDENTS===========")

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

        for student in students:
            if student["student_id"] == student_id:
                display_student(student)
                return

        print("\nStudent not found❌")

    elif choice == "2":
        name = input("Enter student name: ").strip().lower()

        found = False

        for student in students:
            if name in student["name"].lower():
                display_student(student)
                found = True

        if not found:
            print("\nSTUDENT NOT FOUND!!!")

    elif choice == "3":
        department = get_department()

        found = False

        for student in students:
            if student["department"] == department:
                display_student(student)
                found = True

        if not found:
            print("\nNo students found in this department. ❌")



    elif choice == "4":
        print("\nSelect Semester:")
        semester = get_semester()

        found=False

        for student in students:
            if student["semester"] == semester:
                display_student(student)
                found=True
        if not found:
                print ("STUDENT NOT FOUND IN CURRENT SEMESTER..!!❌")

    elif choice == "5":
        print("\nSelect CGPA Range:")

        minimum, maximum = get_cgpa_range()

        found = False

        for student in students:
            if minimum <= student["CGPA"] <= maximum:
                display_student(student)
                found = True

        if not found:
            print("\nNo Student Found in this CGPA Range..❌")

    elif choice == "6":
        minimum, maximum = get_percentage_range()

        found = False

        for student in students:
            if "percentage" in student:
                if minimum <= student["percentage"] <= maximum:
                    display_student(student)
                    found = True

        if not found:
            print("\nNo Student Found in this Percentage Range..❌")

    elif choice == "7":
        minimum, maximum = get_semester_range()

        found = False

        for student in students:
            if minimum <= student["semester"] <= maximum:
                display_student(student)
                found = True

        if not found:
            print("\nNo Student Found in this Semester Range..❌")

    else:
        print("\ninvalid Search Choice!!❌")


#DISPLAY ONE STUDENT
#========================
def display_student(student):
    print("\n========== STUDENT ==========")

    print(f"ID: {student['student_id']}")
    print(f"Name: {student['name']}")
    print(f"Email: {student['email']}")
    print(f"Phone: {student['phone']}")
    print(f"Department: {student['department']}")
    print(f"Semester: {student['semester']}")
    print(f"CGPA: {student['CGPA']}")

    if "marks" in student:
        print("----- Academic Result -----")

        for subject, marks in student["marks"].items():
            print(f"{subject}: {marks}")

        print(f"Total Marks: {student['total_marks']}/{student['maximum_marks']}")
        print(f"Percentage: {student['percentage']:.2f}%")
        print(f"Grade: {student['grade']}")

    else:
        print("Academic Result: Not Available....❌3")



#DELETE STUDENTS
#====================
def delete_students(students):
    student_id = input("Enter student id: ").strip()
    for student in students:
        if student["student_id"] == student_id:

            print ("Student Found : ")
            display_student(student)

            confirm =input ("Do you want to delete student ? y/n").lower()
            if confirm == "y":
                (students.remove(student))
                save_students(students)

                print ("Student Deleted Successfully!👏")

            else:
                print ("\nDelete Cancelled.")
            return
    print(f'\nStudent Not Found!!')

#STATISTICS
#===============
def statistics(students):
    if not students:
        print ("\nno Students Available . ")
        return

    total_students= len(students)

    total_cgpa = sum(student["CGPA"] for student in students)

    average_cgpa = total_cgpa / total_students

    highest_cgpa = max(students,key=lambda student: student["CGPA"])

    lowest_cgpa = min(students,key=lambda student: student["CGPA"])

    students_with_results = [
        student for student in students
        if "percentage" in student and "grade" in student
    ]

    if students_with_results:
        total_percentage = sum(
            student["percentage"] for student in students_with_results
        )

        average_percentage = total_percentage / len(students_with_results)

        grade_counts = {}

        for student in students_with_results:
            grade = student["grade"]
            grade_counts[grade] = grade_counts.get(grade, 0) + 1

    print ("\n=============STATISTICS=============")
    print(f"Total Students: {total_students}")
    print(f"Total cgpa: {total_cgpa}")
    print(f"Average cgpa: {average_cgpa}")
    print(f"Highest cgpa: {highest_cgpa['CGPA']}   "
          f"{highest_cgpa['name']}")
    print(f"Lowest cgpa: {lowest_cgpa['CGPA']}   "
          f"{lowest_cgpa['name']}")

    if students_with_results:
        print(f"Average Percentage: {average_percentage:.2f}%")

        print("Grade Distribution:")

        for grade, count in sorted(grade_counts.items()):
            print(f"{grade}: {count} student(s)")
    else:
        print("Average Percentage: Not Available")
        print("Grade Distribution: Not Available")


#UPDATE STUDENTS
#==================
def update_students(students):
    student_id = get_student_id()
    for student in students:

        if student["student_id"] == student_id:

            print ("\nSTUDENT FOUND....✅")
            print ("ENTER NEW INFORMATION.....")

            student["name"] = get_name()
            student["department"] = get_department()

            email = get_email()

            for other_student in students:
                if other_student is not student:
                    if other_student["email"].lower() == email.lower():
                        print("EMAIL ALREADY EXISTS !!...❌")
                        return

            student["email"] = email

            phone = get_phone()

            for other_student in students:
                if other_student is not student:
                    if other_student["phone"] == phone:
                        print("PHONE NUMBER ALREADY EXISTS !!...❌")
                        return

            student["phone"] = phone

            student["semester"] = get_semester()
            student["CGPA"] = get_cgpa()
            marks = get_subject_marks()
            total_marks, maximum_marks, percentage, grade = calculate_result(marks)

            student["marks"] = marks
            student["total_marks"] = total_marks
            student["maximum_marks"] = maximum_marks
            student["percentage"] = percentage
            student["grade"] = grade

            save_students(students)

            print ("STUDENT UPDATED SUCCESSFULLY !!")

            return

    print(f'\nStudent Not Found!!')

#SORT STUDENTS BY CGPA
#==========================
def sort_by_cgpa(students):

    if not students:
        print ("\nno Students Available . ")
        return

    sorted_students = sorted(students , key=lambda student:student['CGPA'],
    reverse=True)

    print ("=========STUDENTS NY cgpa===========")

    for student in sorted_students:
        print(f"{student['name']} ->"
              f"{student['CGPA']} CGPA ")

#SORTING BY NAME
#======================
def sort_by_name(students):
    if not students:
        print("\nNo Students Available.")
        return

    sorted_students = sorted(
        students,
        key=lambda student: student["name"].lower()
    )

    print("\n========= STUDENTS BY NAME =========")

    for student in sorted_students:
        print(f"{student['name']} -> "
              f"{student['CGPA']} CGPA")

#SORTING BY SEMESTER
#========================
def sort_by_semester(students):
    if not students:
        print("\nNo Students Available.")
        return

    sorted_students = sorted(
        students,
        key=lambda student: student["semester"]
    )

    print("\n========= STUDENTS BY SEMESTER =========")

    for student in sorted_students:
        print(f"{student['name']} -> "
              f"Semester {student['semester']}")


def sort_by_percentage(students):
    students_with_results = [
        student for student in students
        if "percentage" in student
    ]

    if not students_with_results:
        print("\nNo Student Results Available.")
        return

    sorted_students = sorted(
        students_with_results,
        key=lambda student: student["percentage"],
        reverse=True
    )

    print("\n========= STUDENTS BY PERCENTAGE =========")

    for student in sorted_students:
        print(
            f"{student['name']} -> "
            f"{student['percentage']:.2f}% "
            f"({student['grade']})"
        )


#SORTING STUDENTS
#=====================
def sort_students(students):
    if not students:
        print("\nNo Students Available.")
        return

    print("\n========== SORT STUDENTS ==========")
    print("1. Sort by CGPA")
    print("2. Sort by Name")
    print("3. Sort by Semester")
    print("4. Sort by Percentage")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        sort_by_cgpa(students)

    elif choice == "2":
        sort_by_name(students)

    elif choice == "3":
        sort_by_semester(students)

    elif choice == "4":
        sort_by_percentage(students)

    else:
        print("\nInvalid sorting choice! ❌")


#GET MARKS FOR SUBJECT
#========================
def get_subject_marks():
    subjects=[
        "Python",
        "DBMS",
        "Statistics",
        "Mathematics",
        "Calculus",
        "DLD"
    ]
    marks={}
    for subject in subjects:
        marks[subject]=get_marks(subject)
    return marks

