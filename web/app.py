from flask import Flask, jsonify, request
import mysql.connector
import os
import time

app = Flask(__name__)

# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def get_db():
    retries = 5
    while retries > 0:
        try:
            return mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'db'),
                user=os.getenv('MYSQL_USER', 'appuser'),
                password=os.getenv('MYSQL_PASSWORD', 'apppass123'),
                database=os.getenv('MYSQL_DATABASE', 'appdb'),
                connect_timeout=5
            )
        except mysql.connector.Error:
            retries -= 1
            if retries == 0:
                raise
            time.sleep(2)

@app.route('/')
def index():
    return '<h1>Multi-Container App</h1><p>Flask + MySQL on Docker</p>'

@app.route('/api/health')
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except:
        return jsonify({"status": "unhealthy"}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"users": users})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    # Input validation
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email required"}), 400
    if len(data['name']) > 100 or len(data['email']) > 100:
        return jsonify({"error": "Input too long"}), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": user_id, "message": "User created"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        return jsonify({"error": "Database error"}), 500

@app.route('/api/stats')
def stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return jsonify({"total_users": count, "database": "appdb"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
