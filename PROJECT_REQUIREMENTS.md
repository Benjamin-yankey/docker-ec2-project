# Project Requirements

## Task Definition

**Objective**: Use Docker Compose to deploy a two-tier app (Flask/Node.js + MySQL) on EC2.

## Requirements Checklist

### Infrastructure
- [x] EC2 instance (Amazon Linux 2)
- [x] Docker v25+ installed
- [x] Docker Compose v2+ installed
- [x] AWS Free Tier compatible

### Project Structure
- [x] `docker-compose.yml` - Service orchestration
- [x] `web/app.py` - Flask application
- [x] `web/requirements.txt` - Python dependencies
- [x] `web/Dockerfile` - Web container image
- [x] `db/init.sql` - Database initialization
- [x] Alternative: Node.js version in `nodejs-version/`

### Docker Compose Configuration
- [x] Service: `web` (Flask/Node.js)
- [x] Service: `db` (MySQL)
- [x] Environment variables for database
- [x] Port mapping (5000:5000 or 3000:3000)
- [x] Volume for database persistence
- [x] Network configuration

### Verification
- [x] Accessible via `curl http://localhost:5000`
- [x] API endpoints functional
- [x] Database connectivity working
- [x] Cleanup with `docker-compose down --volumes`

## Deliverables

### Required Files
1. `docker-compose.yml` - Container orchestration
2. `app.py` or `app.js` - Application source code
3. `requirements.txt` or `package.json` - Dependencies
4. `init.sql` - Database schema and seed data
5. Evidence of run (screenshots and documentation)

### Evidence Required
- Screenshots of:
  - EC2 instance running
  - `docker-compose ps` output
  - Application accessible on port 5000
  - API responses
- Log files:
  - Container logs
  - API test results
- Documentation:
  - Deployment steps
  - Testing procedures

### Submission Format
- GitHub Repository with all files
- README with setup instructions
- Evidence in `evidence/` directory
- Screenshots in `screenshots/` directory

## Verification Commands

```bash
# Deploy
docker-compose up -d --build

# Verify
curl http://localhost:5000
docker-compose ps

# Cleanup
docker-compose down --volumes
```

## Tools Required
- Docker v25+
- Docker Compose v2+
- AWS EC2 (Amazon Linux 2)
- Git for version control
