# EC2 Deployment Guide - Amazon Linux 2

Step-by-step guide for deploying the multi-container application on AWS EC2.

## Step 1: Launch EC2 Instance

1. Log into AWS Console
2. Navigate to EC2 Dashboard
3. Click "Launch Instance"
4. Configure:
   - **Name**: docker-app-server
   - **AMI**: Amazon Linux 2 AMI (HVM)
   - **Instance Type**: t2.micro (Free Tier)
   - **Key Pair**: Create or select existing
   - **Storage**: 8 GB gp2

### Security Group Configuration

Inbound rules:

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | Your IP |
| Custom TCP | TCP | 5000 | 0.0.0.0/0 |

## Step 2: Connect to Instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

## Step 3: Install Docker & Docker Compose

```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again
exit
```

SSH back in:
```bash
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>

# Verify installation
docker --version
docker-compose --version
```

## Step 4: Deploy Application

### Upload Project Files

```bash
# On local machine:
scp -i your-key.pem -r docker-ec2-project ec2-user@<EC2-IP>:~/

# Or clone from GitHub:
git clone <your-repo-url>
cd docker-ec2-project
```

### Deploy

```bash
cd docker-ec2-project

# Build and start containers
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Step 5: Verify Deployment

```bash
# Test locally on EC2
curl http://localhost:5000
curl http://localhost:5000/api/health
curl http://localhost:5000/api/users

# From your local machine
curl http://<EC2-PUBLIC-IP>:5000
```

Open browser: `http://<EC2-PUBLIC-IP>:5000`

## Step 6: Collect Evidence

```bash
# Container status
docker-compose ps > evidence/docker-ps.txt

# Logs
docker-compose logs web > evidence/docker-logs-web.txt
docker-compose logs db > evidence/docker-logs-db.txt

# API responses
curl http://localhost:5000/api/health > evidence/api-health.txt
curl http://localhost:5000/api/users > evidence/api-users.txt

# Or use script
./collect-evidence.sh
```

## Step 7: Cleanup

```bash
# Stop and remove containers with volumes
docker-compose down --volumes

# Verify cleanup
docker-compose ps
docker volume ls

# Terminate EC2 instance (AWS Console)
```

## Troubleshooting

### Containers not starting
```bash
docker-compose logs
docker-compose restart
```

### Port already in use
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Database connection issues
```bash
docker-compose exec db mysqladmin ping -h localhost -u root -prootpass123
docker-compose restart db
```

## Cost Management

- t2.micro: Free Tier (750 hours/month)
- Stop instance when not in use
- Monitor AWS Billing Dashboard
