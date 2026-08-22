import json



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
def save_students():
    with open('students.json', 'w') as json_file:
        json.dump(students , json_file , indent=4)

#LOAD EXISTING STUDENTS WHEN PROGRAM STARTS
students = load_students()

def get_non_empty_input(message):
    while True:

        value=input(message).strip()
        if value :
            return value

        print("IT CAN'T BE EMPTY !!!!🤞")

#GET STUDENTS CGPA
#====================
def get_cgpa():
    while True:
        try:
            cgpa = float(input("Please enter your cgpa: "))

            if 0<=cgpa<=4.00 :
                return cgpa

            print ("CGPA MUST BE IN RANGE !!🙄")

        except ValueError:
            print ("Please ENTER A VALID NUMBER........😵")

#GET SEMESTER OF STUDENT
#===========================
def get_semester():
    while True:
        try:
            semester= int(input("Please enter your semester: "))

            if 1<=semester<=8:
                return semester

            print ("SEMESTER MUST BE B/W 1-8....")

        except ValueError:
            print ("ENTER A VALID NUMBER FOR SEMESTER.....")

#GET DEPARTMENT OF STUDENT
#============================
def get_department():
    print("\nSelect Department:")
    print("1. Data Science")
    print("2. Computer Science")
    print("3. Software Engineering")
    print("4. Information Technology")

    while True:
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            return "Data Science"

        elif choice == "2":
            return "Computer Science"

        elif choice == "3":
            return "Software Engineering"

        elif choice == "4":
            return "Information Technology"

        else:
            print("Invalid choice! Please select 1-4. ❌")


#ADD STUDENTS
#==================
def add_students():

    print ("\n=====Add students======")

    student_id = get_non_empty_input("Enter student id: ")

    #Check duplicate ID in it
    for student in students:
        if student["student_id"] == student_id:
            print ("STUDENT ALREADY EXIST !!...☠️")
            return

    name = get_non_empty_input("Please enter student name: ")

    department = get_department()

    semester = get_semester()
    cgpa = get_cgpa()

    student={
        "student_id":student_id,
        "name":name,
        "department":department,
        "semester":semester,
        "CGPA":cgpa
    }
    students.append(student)

    save_students()

    print ("\n=====Student added successfully!======")

#VIEW STUDENTS
#=====================
def view_students():
    if not students:
        print ("STUDENT NOT FOUND!!!")
        return

    print ("\n==========Students===========")
    for student in students:
        print(f'id : {student["student_id"]}')
        print(f'name: {student["name"]}')
        print(f'department: {student["department"]}')
        print(f'semester: {student["semester"]}')
        print(f'CGPA: {student["CGPA"]}')
        print(f'---------------------------------------')

#SEARCH STUDENTS
#====================
def search_students():

    if not students:
        print ("\nSTUDENT NOT FOUND!!!❌")
        return

    print ("\n==========SEARCH STUDENTS===========")

    print("1. SEARCH BY ID.... ")
    print("2. SEARCH BY NAME... ")
    print ("3. SEARCH BY DEPARTMENT... ")
    print("4. SEARCH BY SEMESTER... ")

    choice = input ("enter choice : ")

    if choice == "1":

        student_id = input ("Enter student id ").strip()

        for student in students:
            if student["student_id"] == student_id:

                display_student(student)
                return

        print("\nStudent not found❌")

    elif choice == "2":
        name = input ("Enter student name ").strip().lower()
        found = False
        for student in students:
            if student["name"].lower() == name:
                display_student(student)
                found = True

        if not found:

            print ("\nSTUDENT NOT FOUND!!!")

    elif choice == "3":
        print("\nSelect Department:")
        print("1. Data Science")
        print("2. Computer Science")
        print("3. Software Engineering")
        print("4. Information Technology")

        department_choice = input("Enter choice: ")

        if department_choice == "1":
            department = "Data Science"

        elif department_choice == "2":
            department = "Computer Science"

        elif department_choice == "3":
            department = "Software Engineering"

        elif department_choice == "4":
            department = "Information Technology"

        else:
            print("\nInvalid department choice! ❌")
            return

        found = False

        for student in students:
            if student["department"] == department:
                display_student(student)
                found = True

        if not found:
            print("\nNo students found in this department. ❌")

    elif choice == "4":
        print("\nSelect Semester:")
        semester = int(input("enter the semester : "))

        found=False

        for student in students:
            if student["semester"] == semester:
                display_student(student)
                found=True
        if not found:
                print ("STUDENT NOT FOUND IN CURRENT SEMESTER..!!❌")


#DISPLAY ONE STUDENT
#========================
def display_student(student):
    print("\n========== STUDENT ==========")

    print(f"ID: {student['student_id']}")
    print(f"Name: {student['name']}")
    print(f"Department: {student['department']}")
    print(f"Semester: {student['semester']}")
    print(f"CGPA: {student['CGPA']}")



#DELETE STUDENTS
#====================
def delete_students():
    student_id = input("Enter student id: ").strip()
    for student in students:
        if student["student_id"] == student_id:

            print ("Student Found : ")
            display_student(student)

            confirm =input ("Do you want to delete student ? y/n").lower()
            if confirm == "y":
                (students.remove(student))
                save_students()

                print ("Student Deleted Successfully!👏")

            else:
                print ("\nDelete Cancelled.")
            return
    print(f'\nStudent Not Found!!')

#STATISTICS
#===============
def statistics():
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
          f"({highest_cgpa['name']}")
    print(f"Lowest cgpa: {lowest_cgpa['CGPA']}"
          f"({lowest_cgpa['name']}")

def sort_by_cgpa():

    if not students:
        print ("\nno Students Available . ")
        return

    sorted_students = sorted(students , key=lambda student:student['CGPA'],
    reverse=True)

    print ("=========STUDENTS NY cgpa===========")

    for student in sorted_students:
        print(f"{student['name']} ->"
              f"({student['CGPA']} CGPA ")

#UPDATE STUDENTS
#==================
def update_students():
    student_id = input("Enter student id: ").strip()

    for student in students:

        if student["student_id"] == student_id:

            print ("\nSTUDENT FOUND....✅")
            print ("ENTER NEW INFORMATION.....")

            student["name"] = get_non_empty_input("Enter new name: ")
            student["department"] = get_non_empty_input("Enter new department: ")
            student["semester"] = get_semester()
            student["CGPA"] = get_cgpa()

            save_students()

            print ("STUDENT UPDATED SUCCESSFULLY !!")

            return
        print(f'\nStudent Not Found!!')

#MAIN PROGRAMM
#==================
def main ():
    while True:
        print (f'=============STUDENT MANAGEMENT SYSTEM===============')
        print ("1. Add students")
        print ("2. View students")
        print("3. Search students")
        print("4. Delete students")
        print("5. Update students")
        print("6. Statistics")
        print("7. Sort by cgpa")
        print("8. Exit")


        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_students()

        elif choice == 2:
            view_students()

        elif choice == 3:
            search_students()

        elif choice == 4:
            delete_students()

        elif choice == 5:
            update_students()

        elif choice == 6:
            statistics()

        elif choice == 7:
            sort_by_cgpa()

        elif choice == 8:
            print ("GOODBYE !!")
            break

        else:
            print("Invalid choice..... Please try again.")

main()
