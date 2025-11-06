from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
app = Flask(__name__)
app.secret_key = '15c5c5a0cec05dcbc587d5d1ff176a6625f489ef9e7b3899c89a63f3b8de1e47'

# --- MySQL Database Configuration ---
db = mysql.connector.connect(
    host="mysql-container",
    user="root",
    password="rootpass",   # change this
    database="flask_db"         # change this
)

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



