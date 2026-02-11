# Deployment Summary

## Project: Multi-Container App on EC2 (Flask + MySQL)

### Infrastructure

- **Platform**: AWS EC2
- **AMI**: Amazon Linux 2
- **Instance Type**: t2.micro (Free Tier)
- **Tools**: Docker v25+, Docker Compose v2+

### Application Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   Web Service   │◄────────┤   DB Service    │
│  Flask:5000     │         │   MySQL:3306    │
│  (app.py)       │         │   (init.sql)    │
└─────────────────┘         └─────────────────┘
```

### Key Files

1. **docker-compose.yml** - Orchestrates web and db services
2. **web/app.py** - Flask application with 5 API endpoints
3. **web/requirements.txt** - Flask and MySQL connector
4. **web/Dockerfile** - Web container image
5. **db/init.sql** - Database schema with sample data

### Deployment Steps

```bash
# 1. Launch EC2 (Amazon Linux 2, t2.micro)
# 2. Install Docker & Docker Compose
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# 3. Deploy application
docker-compose up -d --build

# 4. Verify
curl http://localhost:5000

# 5. Cleanup
docker-compose down --volumes
```
