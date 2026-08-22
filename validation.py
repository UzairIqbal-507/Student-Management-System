def get_non_empty_input(message):
    while True:

        value=input(message).strip()
        if value :
            return value

        print("IT CAN'T BE EMPTY !!!!🤞")

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

def get_name():
    while True:
        name = input("Enter Student Name: ").strip()

        if name and all(char.isalpha() or char.isspace() for char in name):
            return name

        print("Name can only contain letters and spaces.")

def get_email():
    while True:
        email = input("Enter Email: ").strip()

        if "@" in email and "." in email:
            return email

        print("Invalid email! Please enter a valid email.")

def get_phone():
    while True:
        phone = input("Enter Phone: ").strip()

        if phone.isdigit() and len(phone) == 11:
            return phone

        print("Phone must contain exactly 11 digits.")

def get_menu_choice():
    while True:
        try:
            choice=int(input("Enter your choice (1-8): "))
            if 1<=choice<=8:
                return choice
            print ("Choice MUST BE IN RANGE !!!")

        except ValueError:
            print("PLEASE ENTER A VALID NUMBER !!!")

def get_student_id():
    while True:

        student_id = input("Please enter your student ID: ").strip()

        if student_id:
            return student_id

        print ("Student id cannot be Empty!!❌")

def get_search_choice():
    while True:
        choice = input("Enter choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4","5"):
            return choice

        print("Invalid choice! Please select 1-5.")
