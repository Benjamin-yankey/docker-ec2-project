#!/bin/bash
# Collect evidence for submission

echo "📸 Collecting Evidence..."

# Create a directory to store the collected evidence files
mkdir -p evidence

# Save the current status of all containers to a file
echo "Collecting container status..."
docker-compose ps > evidence/docker-ps.txt

# Save the application and database logs to separate files
echo "Collecting logs..."
docker-compose logs web > evidence/docker-logs-web.txt
docker-compose logs db > evidence/docker-logs-db.txt

# Capture responses from the key API endpoints to verify they are working correctly
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
