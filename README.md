# Multi-Container Application Deployment on EC2

Two-tier application (Flask/Node.js + MySQL) deployed using Docker Compose on AWS EC2.

## Project Overview

This project demonstrates multi-container application deployment:
- **Web Application**: Flask (Python) or Node.js (Express) with RESTful API
- **Modern UI**: Responsive gradient design with real-time updates
- **Database**: MySQL 8.0 with persistent storage
- **Orchestration**: Docker Compose
- **Security**: AWS Secrets Manager support (optional)
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
docker compose up -d --build

# Verify (Note: Using port 5001 for macOS compatibility)
curl http://localhost:5001

# Cleanup
docker compose down --volumes
```

**Note**: Port 5001 is used locally (macOS compatibility). On EC2, you can use port 5000.

### EC2 Deployment

1. Launch EC2 instance (Amazon Linux 2, t2.micro)
2. Install Docker + Docker Compose
3. Attach IAM role with `secretsmanager:GetSecretValue` permission (optional)
4. Upload project files
5. **Optional**: Configure AWS Secrets Manager (see below)
6. Run `docker compose up -d --build`
7. Access via `http://<EC2-IP>:5001`
8. Cleanup with `docker compose down --volumes`

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
curl http://localhost:5001
curl http://localhost:5001/api/health
curl http://localhost:5001/api/users

# Create user
curl -X POST http://localhost:5001/api/users \
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

### AWS Secrets Manager (Optional)

```bash
# Create secret
./setup-secrets.sh

# Set environment variable
export AWS_SECRET_NAME=docker-app-db-credentials

# Deploy with Secrets Manager
docker compose up -d --build
```

App automatically uses Secrets Manager if `AWS_SECRET_NAME` is set, otherwise falls back to environment variables.

### Environment Variables

- `AWS_SECRET_NAME`: AWS Secrets Manager secret name (optional)
- `AWS_REGION`: AWS region (default: us-east-1)
- `MYSQL_HOST`: Database host (default: db)
- `MYSQL_USER`: Database user (default: appuser)
- `MYSQL_PASSWORD`: Database password (change for production)
- `MYSQL_DATABASE`: Database name (default: appdb)

**Security Note**: Use `.env.example` as template. Never commit `.env` files with real credentials.

### Ports

- Flask: 5001 (host) → 5000 (container)
- Node.js: 3000
- MySQL: 3306 (internal only)

**Note**: Port 5001 used locally for macOS compatibility. Can use 5000 on EC2.

## Documentation

- [EC2 Deployment Guide](docs/EC2_DEPLOYMENT_GUIDE.md) - Complete EC2 setup
- [Testing Guide](docs/TESTING_GUIDE.md) - Testing procedures
- [CI/CD Setup](CI_CD_SETUP.md) - GitHub Actions pipeline with security scanning
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

**Implemented:**
- ✅ Non-root container users
- ✅ Resource limits (CPU/Memory)
- ✅ Security headers (XSS, CSRF protection)
- ✅ Trivy vulnerability scanning in CI/CD
- ✅ AWS Secrets Manager integration
- ✅ Input validation
- ✅ No new privileges flag
- ✅ Auto EC2 security updates

**Recommended for Production:**
- Restrict EC2 Security Group SSH to your IP only
- Enable HTTPS with Let's Encrypt
- Use VPC with private subnets
- Enable CloudTrail and GuardDuty
- Regular backups (EBS snapshots)
