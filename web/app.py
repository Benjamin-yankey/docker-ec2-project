from flask import Flask, jsonify, request
import mysql.connector
import os
import time
import json
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Middleware to set security-related HTTP headers for all outgoing responses
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Retrieve database credentials from AWS Secrets Manager if configured
def get_secret():
    secret_name = os.getenv('AWS_SECRET_NAME')
    if not secret_name:
        return None
    
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError:
        return None

# Establish a connection to the MySQL database with retry logic
def get_db():
    secret = get_secret()
    # Use secrets from AWS if available, otherwise fall back to environment variables
    if secret:
        host = secret.get('host', os.getenv('MYSQL_HOST', 'db'))
        user = secret.get('username', os.getenv('MYSQL_USER', 'appuser'))
        password = secret.get('password', os.getenv('MYSQL_PASSWORD', 'apppass123'))
        database = secret.get('database', os.getenv('MYSQL_DATABASE', 'appdb'))
    else:
        host = os.getenv('MYSQL_HOST', 'db')
        user = os.getenv('MYSQL_USER', 'appuser')
        password = os.getenv('MYSQL_PASSWORD', 'apppass123')
        database = os.getenv('MYSQL_DATABASE', 'appdb')
    
    # Retry connection up to 5 times if the database is not immediately available
    retries = 5
    while retries > 0:
        try:
            return mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                connect_timeout=5
            )
        except mysql.connector.Error:
            retries -= 1
            if retries == 0:
                raise
            time.sleep(2)

# Main route that serves the single-page application frontend
@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>User Management System</title>
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
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            padding: 30px 20px;
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.95;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card h2 {
            color: #36454f;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #77a8a8;
            padding-bottom: 10px;
        }
        .stat-box {
            background: linear-gradient(135deg, #77a8a8 0%, #7e7ce8 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s;
        }
        .stat-box:hover {
            transform: translateY(-5px);
        }
        .stat-box h3 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .stat-box p {
            opacity: 0.95;
            font-size: 1.1em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            color: #36454f;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
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
            width: 100%;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: linear-gradient(135deg, #36454f 0%, #77a8a8 100%);
            margin-top: 10px;
        }
        .user-item {
            background: #f5deb3;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            border-left: 4px solid #77a8a8;
            transition: all 0.3s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .user-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .user-info {
            flex: 1;
        }
        .user-item strong {
            color: #36454f;
            font-size: 1.2em;
            display: block;
            margin-bottom: 5px;
        }
        .user-item .email {
            color: #666;
            margin-top: 5px;
        }
        .user-item .date {
            color: #999;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .user-actions {
            display: flex;
            gap: 10px;
        }
        .btn-delete {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
        }
        .btn-delete:hover {
            background: #c82333;
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
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        .empty-state svg {
            width: 100px;
            height: 100px;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        .search-box {
            margin-bottom: 20px;
        }
        .search-box input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
        }
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #77a8a8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .info-box p {
            color: #36454f;
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>User Management System</h1>
            <p>Manage users efficiently with real-time updates</p>
        </div>

        <div class="grid-container">
            <div class="card">
                <h2>📊 System Overview</h2>
                <div id="stats" style="display: grid; gap: 15px;">
                    <div class="stat-box">
                        <h3>-</h3>
                        <p>Loading...</p>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>➕ Add New User</h2>
                <div id="message"></div>
                <form id="userForm">
                    <div class="form-group">
                        <label for="name">Full Name *</label>
                        <input type="text" id="name" placeholder="Enter full name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email Address *</label>
                        <input type="email" id="email" placeholder="Enter email address" required>
                    </div>
                    <button type="submit" class="btn">Add User</button>
                    <button type="button" class="btn btn-secondary" onclick="clearForm()">Clear Form</button>
                </form>
            </div>
        </div>

        <div class="card">
            <h2>👥 User Directory</h2>
            <div class="info-box">
                <p><strong>Total Users:</strong> <span id="userCount">0</span></p>
                <p><strong>Database:</strong> MySQL 8.0</p>
                <p><strong>Status:</strong> <span id="dbStatus">Connected</span></p>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search users by name or email..." onkeyup="filterUsers()">
            </div>
            <div id="users" class="loading">Loading users...</div>
        </div>
    </div>

    <script>
        let allUsers = [];

        function loadStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('stats').innerHTML = `
                        <div class="stat-box">
                            <h3>${data.total_users}</h3>
                            <p>Total Users</p>
                        </div>
                    `;
                    document.getElementById('userCount').textContent = data.total_users;
                })
                .catch(() => {
                    document.getElementById('stats').innerHTML = `
                        <div class="stat-box">
                            <h3>0</h3>
                            <p>Total Users</p>
                        </div>
                    `;
                });
        }

        function loadUsers() {
            fetch('/api/users')
                .then(r => r.json())
                .then(data => {
                    allUsers = data.users;
                    displayUsers(allUsers);
                })
                .catch(() => {
                    document.getElementById('users').innerHTML = '<p class="loading">Error loading users</p>';
                });
        }

        function displayUsers(users) {
            if (users.length === 0) {
                document.getElementById('users').innerHTML = `
                    <div class="empty-state">
                        <svg fill="#999" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                        <h3>No Users Yet</h3>
                        <p>Add your first user using the form above</p>
                    </div>
                `;
            } else {
                const html = users.map(u => {
                    const date = new Date(u.created_at).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                    return `
                        <div class="user-item" data-id="${u.id}">
                            <div class="user-info">
                                <strong>${u.name}</strong>
                                <div class="email">📧 ${u.email}</div>
                                <div class="date">📅 Added: ${date}</div>
                            </div>
                            <div class="user-actions">
                                <button class="btn-delete" onclick="deleteUser(${u.id}, '${u.name}')">Delete</button>
                            </div>
                        </div>
                    `;
                }).join('');
                document.getElementById('users').innerHTML = html;
            }
        }

        function filterUsers() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const filtered = allUsers.filter(u => 
                u.name.toLowerCase().includes(searchTerm) || 
                u.email.toLowerCase().includes(searchTerm)
            );
            displayUsers(filtered);
        }

        function clearForm() {
            document.getElementById('userForm').reset();
            document.getElementById('message').innerHTML = '';
        }

        document.getElementById('userForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            
            if (!name || !email) {
                document.getElementById('message').innerHTML = 
                    '<div class="alert alert-error">Please fill in all fields</div>';
                return;
            }
            
            fetch('/api/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, email})
            })
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('message').innerHTML = 
                        `<div class="alert alert-error">❌ ${data.error}</div>`;
                } else {
                    document.getElementById('message').innerHTML = 
                        '<div class="alert alert-success">✓ User added successfully!</div>';
                    clearForm();
                    loadUsers();
                    loadStats();
                    setTimeout(() => {
                        document.getElementById('message').innerHTML = '';
                    }, 3000);
                }
            })
            .catch(() => {
                document.getElementById('message').innerHTML = 
                    '<div class="alert alert-error">❌ Failed to add user</div>';
            });
        });

        // Check health
        fetch('/api/health')
            .then(r => r.json())
            .then(data => {
                document.getElementById('dbStatus').textContent = 
                    data.status === 'healthy' ? '✓ Connected' : '✗ Disconnected';
            });

        function deleteUser(userId, userName) {
            if (!confirm(`Are you sure you want to delete ${userName}?`)) {
                return;
            }
            
            fetch(`/api/users/${userId}`, {
                method: 'DELETE'
            })
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    loadUsers();
                    loadStats();
                }
            })
            .catch(() => {
                alert('Failed to delete user');
            });
        }

        loadStats();
        loadUsers();
        setInterval(loadStats, 10000);
        setInterval(loadUsers, 30000);
    </script>
</body>
</html>'''

# Health check endpoint to verify database connectivity
@app.route('/api/health')
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except:
        return jsonify({"status": "unhealthy"}), 500

# Endpoint to retrieve the list of all users
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"users": users})

# Endpoint to create a new user with validation and error handling
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    # Validate that both name and email are provided
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email required"}), 400
    # Limit input length to prevent potential database issues
    if len(data['name']) > 100 or len(data['email']) > 100:
        return jsonify({"error": "Input too long"}), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": user_id, "message": "User created"}), 201
    except mysql.connector.IntegrityError:
        # Handle duplicate email entries (unique constraint in database)
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        return jsonify({"error": "Database error"}), 500

# Endpoint to retrieve system-wide statistics
@app.route('/api/stats')
def stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return jsonify({"total_users": count, "database": "appdb"})

# Endpoint to delete a specific user by their unique ID
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        if affected == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Database error"}), 500

# Entry point for running the Flask application
if __name__ == '__main__':
    # Listen on all available network interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)
