from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import time
from mysql.connector import Error
app = Flask(__name__)
app.secret_key = '15c5c5a0cec05dcbc587d5d1ff176a6625f489ef9e7b3899c89a63f3b8de1e47'

# Retry settings
max_retries = 10
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        db = mysql.connector.connect(
            host="db",           # Service name from Docker Compose
            user="root",
            password="rootpass",
            database="flask_db"
        )
        print("Connected to MySQL!")
        break  # Success, exit the loop
    except Error as e:
        print(f"Attempt {attempt + 1}: MySQL not ready, retrying in {retry_delay}s...")
        time.sleep(retry_delay)
else:
    # If all retries fail
    print("Failed to connect to MySQL after several attempts.")
    exit(1)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return render_template('after_login_dashboard.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = db.cursor()
        # ✅ Check if user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return render_template('login.html')
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, password, email)
        )
        db.commit()

        return "User registered successfully!"
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)



