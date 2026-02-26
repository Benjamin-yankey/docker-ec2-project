const express = require('express');
const mysql = require('mysql2/promise');

const app = express();
// Enable JSON body parsing with a 1MB limit
app.use(express.json({ limit: '1mb' }));

// Middleware to set standard security headers for all responses
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    next();
});

// Database connection configuration using environment variables
const dbConfig = {
    host: process.env.MYSQL_HOST || 'db',
    user: process.env.MYSQL_USER || 'appuser',
    password: process.env.MYSQL_PASSWORD || 'apppass123',
    database: process.env.MYSQL_DATABASE || 'appdb'
};

// Default route to verify the application is running
app.get('/', (req, res) => {
    res.send('<h1>Multi-Container App</h1><p>Node.js + MySQL on Docker</p>');
});

// Health check endpoint to verify database connectivity
app.get('/api/health', async (req, res) => {
    try {
        const conn = await mysql.createConnection(dbConfig);
        await conn.end();
        res.json({ status: 'healthy', database: 'connected' });
    } catch (err) {
        res.status(500).json({ status: 'unhealthy' });
    }
});

// Endpoint to retrieve all users from the database
app.get('/api/users', async (req, res) => {
    const conn = await mysql.createConnection(dbConfig);
    const [rows] = await conn.execute('SELECT * FROM users');
    await conn.end();
    res.json({ users: rows });
});

// Endpoint to create a new user
app.post('/api/users', async (req, res) => {
    const { name, email } = req.body;
    
    // Validate that both name and email are provided
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email required' });
    }
    // Limit input length to prevent potential database issues
    if (name.length > 100 || email.length > 100) {
        return res.status(400).json({ error: 'Input too long' });
    }
    
    try {
        const conn = await mysql.createConnection(dbConfig);
        // Execute the insert query using parameterized values to prevent SQL injection
        const [result] = await conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', [name, email]);
        await conn.end();
        res.status(201).json({ id: result.insertId, message: 'User created' });
    } catch (err) {
        // Handle duplicate email entries
        if (err.code === 'ER_DUP_ENTRY') {
            return res.status(409).json({ error: 'Email already exists' });
        }
        res.status(500).json({ error: 'Database error' });
    }
});

// Endpoint to get the total user count
app.get('/api/stats', async (req, res) => {
    const conn = await mysql.createConnection(dbConfig);
    const [rows] = await conn.execute('SELECT COUNT(*) as count FROM users');
    await conn.end();
    res.json({ total_users: rows[0].count, database: 'appdb' });
});

// Start the server on port 3000
app.listen(3000, () => console.log('Server running on port 3000'));
