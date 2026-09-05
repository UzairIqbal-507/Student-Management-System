import json
import os
import psycopg2
from psycopg2.extras import Json
from database import DB_CONFIG, init_db, get_db_connection

def migrate_json_to_postgres(json_filepath="students.json"):
    # 1. Check if JSON file exists
    if not os.path.exists(json_filepath):
        print(f"❌ Error: '{json_filepath}' file nahi mili!")
        return

    # 2. Ensure Database & Tables are initialized
    init_db()

    # 3. Read JSON Data
    try:
        with open(json_filepath, "r", encoding="utf-8") as file:
            students = json.load(file)
            print(f"📄 Found {len(students)} students in '{json_filepath}'. Starting migration...")
    except Exception as e:
        print(f"❌ JSON file read karne mein error aaya: {e}")
        return

    if not students:
        print("⚠️ JSON file khali (empty) hai. Migration skipped.")
        return

    # 4. Connect to PostgreSQL and Insert Data
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        inserted_count = 0
        skipped_count = 0

        for student in students:
            # Safely handle key names (CGPA vs cgpa)
            cgpa = student.get("CGPA") if "CGPA" in student else student.get("cgpa", 0.0)
            marks = student.get("marks", {})

            cursor.execute('''
                INSERT INTO students (
                    student_id, name, email, phone, department, 
                    semester, cgpa, marks_json, total_marks, 
                    maximum_marks, percentage, grade
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (student_id) DO NOTHING;
            ''', (
                student.get("student_id"),
                student.get("name"),
                student.get("email"),
                student.get("phone"),
                student.get("department"),
                student.get("semester"),
                cgpa,
                Json(marks),
                student.get("total_marks"),
                student.get("maximum_marks"),
                student.get("percentage"),
                student.get("grade")
            ))

            # Check if row was inserted or ignored due to duplicate ID
            if cursor.rowcount > 0:
                inserted_count += 1
            else:
                skipped_count += 1

        conn.commit()
        cursor.close()

        print("\n==========================================")
        print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print(f"✅ Records Inserted : {inserted_count}")
        print(f"⚠️ Records Skipped  : {skipped_count} (Already existed in DB)")
        print("==========================================\n")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n❌ Database Migration Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_json_to_postgres()