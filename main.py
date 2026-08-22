from utils import load_students
from validation import get_menu_choice

from student_manager import (
    add_students,
    view_students,
    search_students,
    update_students,
    delete_students,
    statistics,
    sort_by_cgpa
)



#LOAD EXISTING STUDENTS WHEN PROGRAM STARTS
students = load_students()

#MAIN PROGRAM
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


        choice = get_menu_choice()
        if choice == 1:
            add_students(students)

        elif choice == 2:
            view_students(students)

        elif choice == 3:
            search_students(students)

        elif choice == 4:
            delete_students(students)

        elif choice == 5:
            update_students(students)

        elif choice == 6:
            statistics(students)

        elif choice == 7:
            sort_by_cgpa(students)

        elif choice == 8:
            print ("GOODBYE !!")
            break

        else:
            print("Invalid choice..... Please try again.")

main()
