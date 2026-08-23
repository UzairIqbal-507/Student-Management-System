def get_non_empty_input(message):
    while True:

        value=input(message).strip()
        if value :
            return value

        print("IT CAN'T BE EMPTY !!!!🤞")



#GET NAME OF STUDENT
#=========================
def get_name():
    while True:
        name = input("Enter Student Name: ").strip()

        if name and all(char.isalpha() or char.isspace() for char in name):
            return name

        print("Name can only contain letters and spaces.")

#GET EMAIL OF STUDENT
#=========================
def get_email():
    while True:
        email = input("Enter Email: ").strip()

        if "@" in email and "." in email:
            return email

        print("Invalid email! Please enter a valid email.")

#GET PHONE OF STUDENT
#=========================
def get_phone():
    while True:
        phone = input("Enter Phone: ").strip()

        if phone.isdigit() and len(phone) == 11:
            return phone

        print("Phone must contain exactly 11 digits.")

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



#GET STUDENTS cgpa
#====================
def get_cgpa():
    while True:
        try:
            cgpa = float(input("Please enter your cgpa: "))

            if 0<=cgpa<=4.00 :
                return cgpa

            print ("cgpa MUST BE IN RANGE !!🙄")

        except ValueError:
            print ("Please ENTER A VALID NUMBER........😵")

def get_marks(subject):
    while True:
        try:
            marks = float(input(f"Please enter marks for {subject} (0-100)"))
            if 0<=marks<=100:
                return marks
            print ("marks MUST BE IN RANGE b/w (0-100) !!!🙄")
        except ValueError:
            print ("PLEASE ENTER A VALID NUMBER !!!😵")

def calculate_result(marks):
    total_marks = sum(marks.values())
    maximum_marks = len(marks) * 100
    percentage = (total_marks / maximum_marks) * 100
    grade = get_grade(percentage)

    return total_marks, maximum_marks, percentage, grade

def get_grade(percentage):
    if percentage >=90:
        return "A+"
    elif percentage >=80:
        return "A"
    elif percentage >=70:
        return "B"
    elif percentage >=60:
        return "C"
    elif percentage >=50:
        return "D"
    else:
        return "F"


#CHOICE FOR MAIN MENU
#=======================
def get_menu_choice():
    while True:
        try:
            choice=int(input("Enter your choice (1-8): "))
            if 1<=choice<=8:
                return choice
            print ("Choice MUST BE IN RANGE !!!")

        except ValueError:
            print("PLEASE ENTER A VALID NUMBER !!!")

#GET ID OF STUDENT
#=========================
def get_student_id():
    while True:

        student_id = input("Please enter your student ID: ").strip()

        if student_id:
            return student_id

        print ("Student id cannot be Empty!!❌")

#SEARCH STUDENTS
#=========================
def get_search_choice():
    while True:
        choice = input("Enter choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4","5"):
            return choice

        print("Invalid choice! Please select 1-5.")
