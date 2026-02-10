#!/bin/bash
# Collect evidence for submission

echo "📸 Collecting Evidence..."

mkdir -p evidence

# Container status
echo "Collecting container status..."
docker-compose ps > evidence/docker-ps.txt

# Logs
echo "Collecting logs..."
docker-compose logs web > evidence/docker-logs-web.txt
docker-compose logs db > evidence/docker-logs-db.txt

# API responses
echo "Testing API endpoints..."
{
  echo "=== Health Check ==="
  curl -s http://localhost:5000/api/health
  echo -e "\n\n=== Users List ==="
  curl -s http://localhost:5000/api/users
  echo -e "\n\n=== Stats ==="
  curl -s http://localhost:5000/api/stats
} > evidence/api-responses.txt

echo "✅ Evidence collected in evidence/ directory"
echo ""
echo "Next steps:"
echo "1. Take screenshots of http://localhost:5000 in browser"
echo "2. Screenshot docker-compose ps output"
echo "3. Screenshot EC2 instance in AWS console"
