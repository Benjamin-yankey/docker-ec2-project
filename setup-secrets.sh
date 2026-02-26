#!/bin/bash

# Configuration for the AWS Secret
SECRET_NAME="docker-app-db-credentials"
REGION="us-east-1"

echo "Creating secret in AWS Secrets Manager..."

# Create a new secret containing database credentials with a randomly generated password
aws secretsmanager create-secret \
  --name "$SECRET_NAME" \
  --description "Database credentials for Docker app" \
  --secret-string '{
    "username":"appuser",
    "password":"'"$(openssl rand -base64 32)"'",
    "host":"db",
    "database":"appdb"
  }' \
  --region "$REGION"

echo "Secret created: $SECRET_NAME"
echo "Update your .env file with: AWS_SECRET_NAME=$SECRET_NAME"
