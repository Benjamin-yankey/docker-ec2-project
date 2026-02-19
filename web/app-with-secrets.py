from flask import Flask, jsonify, request
import mysql.connector
import os
import time

# Optional: AWS Secrets Manager support
try:
    import boto3
    import json
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

app = Flask(__name__)

# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def get_secrets():
    """Get database credentials from AWS Secrets Manager or environment variables"""
    if BOTO3_AVAILABLE and os.getenv('USE_SECRETS_MANAGER', 'false').lower() == 'true':
        try:
            secret_name = os.getenv('SECRET_NAME', 'docker-app/db-credentials')
            region_name = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager', region_name=region_name)
            
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            return json.loads(get_secret_value_response['SecretString'])
        except Exception as e:
            print(f"Warning: Could not fetch from Secrets Manager: {e}")
            print("Falling back to environment variables")
    
    # Fallback to environment variables
    return {
        'MYSQL_HOST': os.getenv('MYSQL_HOST', 'db'),
        'MYSQL_USER': os.getenv('MYSQL_USER', 'appuser'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD', 'apppass123'),
        'MYSQL_DATABASE': os.getenv('MYSQL_DATABASE', 'appdb')
    }

def get_db():
    secrets = get_secrets()
    retries = 5
    while retries > 0:
        try:
            return mysql.connector.connect(
                host=secrets['MYSQL_HOST'],
                user=secrets['MYSQL_USER'],
                password=secrets['MYSQL_PASSWORD'],
                database=secrets['MYSQL_DATABASE'],
                connect_timeout=5
            )
        except mysql.connector.Error:
            retries -= 1
            if retries == 0:
                raise
            time.sleep(2)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Multi-Container App</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #36454f 0%, #77a8a8 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            padding: 30px 20px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stats-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-box {
            background: linear-gradient(135deg, #77a8a8 0%, #7e7ce8 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-box h3 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .stat-box p {
            opacity: 0.9;
        }
        .form-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .form-card h2 {
            color: #333;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            color: #555;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #77a8a8;
        }
        .btn {
            background: linear-gradient(135deg, #77a8a8 0%, #7e7ce8 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .users-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .users-card h2 {
            color: #333;
            margin-bottom: 20px;
        }
        .user-item {
            background: #f5deb3;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid #77a8a8;
            transition: transform 0.2s;
        }
        .user-item:hover {
            transform: translateX(5px);
        }
        .user-item strong {
            color: #333;
            font-size: 1.1em;
        }
        .user-item .email {
            color: #666;
            margin-top: 5px;
        }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Multi-Container Application</h1>
        </div>

        <div class="stats-card">
            <h2>📊 System Statistics</h2>
            <div class="stats-grid" id="stats">
                <div class="stat-box">
                    <h3>-</h3>
                    <p>Loading...</p>
                </div>
            </div>
        </div>

        <div class="form-card">
            <h2>➕ Add New User</h2>
            <div id="message"></div>
            <form id="userForm">
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" placeholder="Enter full name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" placeholder="Enter email address" required>
                </div>
                <button type="submit" class="btn">Add User</button>
            </form>
        </div>

        <div class="users-card">
            <h2>👥 User Directory</h2>
            <div id="users" class="loading">Loading users...</div>
        </div>
    </div>

    <script>
        function loadStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('stats').innerHTML = `
                        <div class="stat-box">
                            <h3>${data.total_users}</h3>
                            <p>Total Users</p>
                        </div>
                        <div class="stat-box">
                            <h3>${data.database}</h3>
                            <p>Database</p>
                        </div>
                        <div class="stat-box">
                            <h3>✓</h3>
                            <p>System Healthy</p>
                        </div>
                    `;
                });
        }

        function loadUsers() {
            fetch('/api/users')
                .then(r => r.json())
                .then(data => {
                    const html = data.users.map(u => `
                        <div class="user-item">
                            <strong>${u.name}</strong>
                            <div class="email">📧 ${u.email}</div>
                        </div>
                    `).join('');
                    document.getElementById('users').innerHTML = html || '<p class="loading">No users found</p>';
                });
        }

        document.getElementById('userForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            
            fetch('/api/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, email})
            })
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('message').innerHTML = 
                        `<div class="alert alert-error">${data.error}</div>`;
                } else {
                    document.getElementById('message').innerHTML = 
                        `<div class="alert alert-success">✓ User added successfully!</div>`;
                    document.getElementById('userForm').reset();
                    loadUsers();
                    loadStats();
                    setTimeout(() => {
                        document.getElementById('message').innerHTML = '';
                    }, 3000);
                }
            });
        });

        loadStats();
        loadUsers();
        setInterval(loadStats, 10000);
    </script>
</body>
</html>'''

@app.route('/api/health')
def health():
    try:
        conn = get_db()
        conn.close()
        secrets_status = "Secrets Manager" if BOTO3_AVAILABLE and os.getenv('USE_SECRETS_MANAGER', 'false').lower() == 'true' else "Environment Variables"
        return jsonify({"status": "healthy", "database": "connected", "credentials": secrets_status})
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
