FROM node:18-slim

WORKDIR /app

# Install security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY package*.json ./
RUN npm install --production && npm cache clean --force

# Copy application
COPY app.js .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 3000

CMD ["npm", "start"]
