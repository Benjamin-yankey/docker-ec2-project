const express = require('express');
const mysql = require('mysql2/promise');

const app = express();
app.use(express.json({ limit: '1mb' }));

// Security headers
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    next();
});

const dbConfig = {
    host: process.env.MYSQL_HOST || 'db',
    user: process.env.MYSQL_USER || 'appuser',
    password: process.env.MYSQL_PASSWORD || 'apppass123',
    database: process.env.MYSQL_DATABASE || 'appdb'
};

app.get('/', (req, res) => {
    res.send('<h1>Multi-Container App</h1><p>Node.js + MySQL on Docker</p>');
});

app.get('/api/health', async (req, res) => {
    try {
        const conn = await mysql.createConnection(dbConfig);
        await conn.end();
        res.json({ status: 'healthy', database: 'connected' });
    } catch (err) {
        res.status(500).json({ status: 'unhealthy' });
    }
});

app.get('/api/users', async (req, res) => {
    const conn = await mysql.createConnection(dbConfig);
    const [rows] = await conn.execute('SELECT * FROM users');
    await conn.end();
    res.json({ users: rows });
});

app.post('/api/users', async (req, res) => {
    const { name, email } = req.body;
    
    // Input validation
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email required' });
    }
    if (name.length > 100 || email.length > 100) {
        return res.status(400).json({ error: 'Input too long' });
    }
    
    try {
        const conn = await mysql.createConnection(dbConfig);
        const [result] = await conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', [name, email]);
        await conn.end();
        res.status(201).json({ id: result.insertId, message: 'User created' });
    } catch (err) {
        if (err.code === 'ER_DUP_ENTRY') {
            return res.status(409).json({ error: 'Email already exists' });
        }
        res.status(500).json({ error: 'Database error' });
    }
});

app.get('/api/stats', async (req, res) => {
    const conn = await mysql.createConnection(dbConfig);
    const [rows] = await conn.execute('SELECT COUNT(*) as count FROM users');
    await conn.end();
    res.json({ total_users: rows[0].count, database: 'appdb' });
});

app.listen(3000, () => console.log('Server running on port 3000'));
