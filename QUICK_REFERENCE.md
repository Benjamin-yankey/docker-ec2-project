# Quick Reference

## Deployment Commands

```bash
# Deploy Flask
./deploy.sh

# Deploy Node.js
./deploy.sh nodejs

# Run tests
./test-deployment.sh
```

## Docker Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Check status
docker compose ps

# Restart service
docker compose restart web
```

## API Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Get users
curl http://localhost:5000/api/users

# Create user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'

# Get stats
curl http://localhost:5000/api/stats
```

## Database Commands

```bash
# Connect to database
docker compose exec db mysql -u appuser -papppass123 appdb

# Run query
docker compose exec db mysql -u appuser -papppass123 appdb -e "SELECT * FROM users;"
```

## Troubleshooting

```bash
# View container logs
docker compose logs web
docker compose logs db

# Restart all services
docker compose restart

# Clean restart
docker compose down -v
docker compose up -d --build
```
