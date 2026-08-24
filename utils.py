import json
import os
from datetime import datetime

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
def save_students(students):

    if os.path.exists('students.json'):
        backup_students()

    with open('students.json', 'w') as json_file:
        json.dump(students, json_file, indent=4)


# BACKUP STUDENTS DATA
# =========================
# BACKUP STUDENTS DATA
# =========================
def backup_students():
    try:
        with open('students.json') as source:
            students = json.load(source)

        os.makedirs('backups', exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        backup_file = f"backups/students_backup_{timestamp}.json"

        with open(backup_file, 'w') as backup:
            json.dump(students, backup, indent=4)

        print(f"\nStudent data backup created: {backup_file} ✅")

    except FileNotFoundError:
        print("\nNo student data available for backup. ❌")

