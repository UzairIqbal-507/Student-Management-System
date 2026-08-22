from validation import (get_non_empty_input, get_semester,
                        get_department, get_cgpa,
                        get_email, get_phone, get_name, get_student_id, get_search_choice)

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
    email= get_email()
    phone = get_phone()

    department = get_department()

    semester = get_semester()
    cgpa = get_cgpa()

    student={
        "student_id":student_id,
        "name":name,
        "email":email,
        "phone":phone,
        "department":department,
        "semester":semester,
        "CGPA":cgpa
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
        print(f'---------------------------------------')

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

    choice = get_search_choice()

    if choice == "1":

        student_id = get_student_id()

        for student in students:
            if student["student_id"] == student_id:
                display_student(student)
                return

        print("\nStudent not found❌")

    elif choice == "2":
        name = get_name().lower()
        found = False
        for student in students:
            if student["name"].lower() == name:
                display_student(student)
                found = True

        if not found:

            print ("\nSTUDENT NOT FOUND!!!")

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
        print("\nSelect CGPA:")
        cgpa = get_cgpa()
        found= False
        for student in students:
            if student["CGPA"] == cgpa:
                display_student(student)
                found=True
        if not found :
            print ("\nNo Student Found with this CGPA..❌")

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

    print ("\n=============STATISTICS=============")
    print(f"Total Students: {total_students}")
    print(f"Total cgpa: {total_cgpa}")
    print(f"Average cgpa: {average_cgpa}")
    print(f"Highest cgpa: {highest_cgpa['CGPA']}"
          f"{highest_cgpa['name']}")
    print(f"Lowest cgpa: {lowest_cgpa['CGPA']}"
          f"{lowest_cgpa['name']}")

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
            student["email"] = get_email()
            student["phone"] = get_phone()
            student["semester"] = get_semester()
            student["CGPA"] = get_cgpa()

            save_students(students)

            print ("STUDENT UPDATED SUCCESSFULLY !!")

            return
        print(f'\nStudent Not Found!!')

