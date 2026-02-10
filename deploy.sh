#!/bin/bash

set -e

echo "🚀 Multi-Container Deployment Script"
echo "===================================="

VERSION="flask"
if [ "$1" == "nodejs" ]; then
    VERSION="nodejs"
fi

echo "📦 Deploying $VERSION version..."

if [ "$VERSION" == "nodejs" ]; then
    docker-compose -f docker-compose-nodejs.yml down -v 2>/dev/null || true
    docker-compose -f docker-compose-nodejs.yml up -d --build
    PORT=3000
else
    docker-compose down -v 2>/dev/null || true
    docker-compose up -d --build
    PORT=5000
fi

echo "⏳ Waiting for services to be ready..."
sleep 15

echo "✅ Deployment complete!"
echo "🌐 Application: http://localhost:$PORT"
echo "🔍 Health check: http://localhost:$PORT/api/health"
echo ""
echo "📊 Container status:"
docker-compose ps 2>/dev/null || docker-compose -f docker-compose-nodejs.yml ps
