#!/bin/bash

echo "🗑️  Destroying Docker resources..."

# Stop and remove containers, networks, and associated volumes
docker compose down --volumes --remove-orphans

# Stop and remove containers, then delete all images used by the services
docker compose down --rmi all --volumes --remove-orphans

# Prompt user to prune the entire Docker system to reclaim disk space
read -p "Remove all unused Docker resources? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker system prune -a --volumes -f
fi

echo "✅ Local cleanup complete"

# Optional step to delete the database credentials secret from AWS
read -p "Delete AWS Secrets Manager secret? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SECRET_NAME="${AWS_SECRET_NAME:-docker-app-db-credentials}"
    aws secretsmanager delete-secret --secret-id "$SECRET_NAME" --force-delete-without-recovery --region "${AWS_REGION:-us-east-1}" 2>/dev/null
    echo "✅ Secret deleted: $SECRET_NAME"
fi

echo "
📝 Manual cleanup required:
- Terminate EC2 instance in AWS Console
- Delete IAM role (if created)
- Delete Security Group (if custom)
- Delete EBS volumes/snapshots
"
