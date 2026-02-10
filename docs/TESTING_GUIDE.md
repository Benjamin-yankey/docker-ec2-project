# Testing Guide

Comprehensive testing procedures for the multi-container application.

## Pre-Deployment Tests

### 1. Verify Docker Installation

```bash
docker --version
docker compose version
```

### 2. Check Project Files

```bash
ls -la
cat docker-compose.yml
cat web/Dockerfile
```

## Deployment Testing

### 1. Build and Start

```bash
./deploy.sh
```

### 2. Verify Containers

```bash
docker compose ps
docker compose logs
```

## API Testing

### Health Check

```bash
curl http://localhost:5000/api/health
```

Expected: `{"status":"healthy","database":"connected"}`

### Get Users

```bash
curl http://localhost:5000/api/users
```

### Create User

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'
```

### Get Stats

```bash
curl http://localhost:5000/api/stats
```

## Automated Testing

```bash
./test-deployment.sh
```

## Database Testing

```bash
docker compose exec db mysql -u appuser -papppass123 appdb -e "SELECT * FROM users;"
```

## Evidence Collection

```bash
docker compose ps > evidence/docker-ps.txt
docker compose logs web > evidence/docker-logs-web.txt
./test-deployment.sh > evidence/api-tests.txt
```
