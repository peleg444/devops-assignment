from flask import Flask, request, make_response
import mysql.connector
import os
from datetime import datetime
import socket

app = Flask(__name__)

# פרטי התחברות לבסיס הנתונים
DB_CONFIG = {
    'host': 'db',  # שם הקונטיינר של mysql
    'user': 'root',
    'password': '123',
    'database': 'app_db'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # יצירת טבלאות אם לא קיימות
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            client_ip VARCHAR(100),
            internal_ip VARCHAR(100),
            access_time DATETIME
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INT PRIMARY KEY,
            count INT
        )
    """)

    # אתחול counter אם הוא ריק
    cursor.execute("INSERT IGNORE INTO counter (id, count) VALUES (1, 0)")

    # הגדלת counter
    cursor.execute("UPDATE counter SET count = count + 1 WHERE id = 1")
    conn.commit()

    # פרטים עבור הלוג
    internal_ip = socket.gethostbyname(socket.gethostname())

    client_ip = request.remote_addr
    now = datetime.now()

    cursor.execute("""
        INSERT INTO access_log (client_ip, internal_ip, access_time)
        VALUES (%s, %s, %s)
    """, (client_ip, internal_ip, now))
    conn.commit()

    cursor.close()
    conn.close()

    # יצירת קוקי
    resp = make_response(f"Internal IP: {internal_ip}")
    resp.set_cookie('server_ip', internal_ip, max_age=300)
    return resp

@app.route('/showcount')
def showcount():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM counter WHERE id = 1")
    result = cursor.fetchone()
    count = result[0] if result else 0
    cursor.close()
    conn.close()
    return f"Global Counter: {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
