# Multi-Container Application Deployment on EC2

Two-tier application (Flask/Node.js + MySQL) deployed using Docker Compose on AWS EC2.

## Project Overview

This project demonstrates multi-container application deployment:
- **Web Application**: Flask (Python) or Node.js (Express) with RESTful API
- **Database**: MySQL 8.0 with persistent storage
- **Orchestration**: Docker Compose
- **Deployment**: AWS EC2 Amazon Linux 2 (Free Tier)

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Web Service   │◄────────┤   DB Service    │
│  Flask:5000     │         │   MySQL:3306    │
└─────────────────┘         └─────────────────┘
```

## Quick Start

### Local Testing

```bash
# Deploy Flask version
docker-compose up -d --build

# Verify
curl http://localhost:5000

# Cleanup
docker-compose down --volumes
```

### EC2 Deployment

1. Launch EC2 instance (Amazon Linux 2, t2.micro)
2. Install Docker + Docker Compose
3. Upload project files
4. Run `docker-compose up -d --build`
5. Access via `http://<EC2-IP>:5000`
6. Cleanup with `docker-compose down --volumes`

See [EC2_DEPLOYMENT_GUIDE.md](docs/EC2_DEPLOYMENT_GUIDE.md) for detailed steps.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/health` | GET | Health check |
| `/api/users` | GET | List all users |
| `/api/users` | POST | Create user |
| `/api/stats` | GET | Database stats |

## Testing

```bash
# Verify deployment
curl http://localhost:5000
curl http://localhost:5000/api/health
curl http://localhost:5000/api/users

# Create user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'

# Collect evidence
./collect-evidence.sh
```

## Project Structure

```
docker-ec2-project/
├── docker-compose.yml          # Flask orchestration
├── docker-compose-nodejs.yml   # Node.js orchestration
├── web/                        # Flask application
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── nodejs-version/             # Node.js application
│   ├── app.js
│   ├── Dockerfile
│   └── package.json
├── db/
│   └── init.sql               # Database schema
├── docs/
│   ├── EC2_DEPLOYMENT_GUIDE.md
│   └── TESTING_GUIDE.md
├── evidence/                   # Test outputs
└── screenshots/                # Visual evidence
```

## Configuration

### Environment Variables

- `MYSQL_HOST`: Database host (default: db)
- `MYSQL_USER`: Database user (default: appuser)
- `MYSQL_PASSWORD`: Database password (change for production)
- `MYSQL_DATABASE`: Database name (default: appdb)

**Security Note**: Use `.env.example` as template. Never commit `.env` files with real credentials.

### Ports

- Flask: 5000
- Node.js: 3000
- MySQL: 3306 (internal only)

## Documentation

- [EC2 Deployment Guide](docs/EC2_DEPLOYMENT_GUIDE.md) - Complete EC2 setup
- [Testing Guide](docs/TESTING_GUIDE.md) - Testing procedures
- [Submission Checklist](SUBMISSION_CHECKLIST.md) - Deliverables
- [Quick Reference](QUICK_REFERENCE.md) - Command cheat sheet

## Technologies

- **Docker**: v25+
- **Docker Compose**: v2+
- **Python**: 3.9 (Flask)
- **Node.js**: 18 (Express)
- **MySQL**: 8.0
- **AWS EC2**: Amazon Linux 2, t2.micro (Free Tier)

## Security

See [SECURITY.md](SECURITY.md) for implemented security measures and best practices.
