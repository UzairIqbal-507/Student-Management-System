import psycopg2

try:
    conn = psycopg2.connect(
        dbname="student_db",
        user="postgres",
        password="Uz@ir507",  # Apna password yahan likhein
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cursor.fetchall()
    print("PostgreSQL Tables Found:", tables)
    conn.close()
except Exception as e:
    print("Connection Failed Error:", e)