#!/bin/bash
# Minimal deployment script for EC2

echo "🚀 Deploying Multi-Container Application"

# Stop existing containers
docker-compose down --volumes 2>/dev/null || true

# Build and start
docker-compose up -d --build

echo "⏳ Waiting for services..."
sleep 15

echo "✅ Deployment complete!"
echo "🌐 Access: http://localhost:5000"
echo ""
echo "📊 Container Status:"
docker-compose ps
