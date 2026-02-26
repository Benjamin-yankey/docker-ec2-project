#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Multi-Container Deployment Script"
echo "===================================="

# Set the application version (flask or nodejs)
VERSION="flask"
if [ "$1" == "nodejs" ]; then
    VERSION="nodejs"
fi

echo "📦 Deploying $VERSION version..."

# Stop and remove existing containers, then build and start new ones based on the selected version
if [ "$VERSION" == "nodejs" ]; then
    docker-compose -f docker-compose-nodejs.yml down -v 2>/dev/null || true
    docker-compose -f docker-compose-nodejs.yml up -d --build
    PORT=3000
else
    docker-compose down -v 2>/dev/null || true
    docker-compose up -d --build
    PORT=5000
fi

# Wait for the database and application services to initialize
echo "⏳ Waiting for services to be ready..."
sleep 15

echo "✅ Deployment complete!"
echo "🌐 Application: http://localhost:$PORT"
echo "🔍 Health check: http://localhost:$PORT/api/health"
echo ""
echo "📊 Container status:"
# Display the status of the running containers
docker-compose ps 2>/dev/null || docker-compose -f docker-compose-nodejs.yml ps
