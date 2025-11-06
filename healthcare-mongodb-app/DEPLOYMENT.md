# Deployment Guide

This guide covers deploying the Healthcare MongoDB Application to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [MongoDB Atlas Setup](#mongodb-atlas-setup)
- [Application Deployment](#application-deployment)
- [Environment Configuration](#environment-configuration)
- [Performance Tuning](#performance-tuning)
- [Monitoring](#monitoring)
- [Security](#security)
- [Backup & Recovery](#backup--recovery)
- [Scaling](#scaling)

---

## Prerequisites

- MongoDB Atlas account (or self-hosted MongoDB 6.0+)
- Node.js 18+ runtime environment
- Production server (AWS, Azure, Google Cloud, DigitalOcean, etc.)
- Domain name (optional)
- SSL certificate (for HTTPS)

---

## MongoDB Atlas Setup

### Step 1: Create Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Verify email address

### Step 2: Create Cluster

1. Click "Build a Cluster"
2. Choose provider (AWS recommended for best performance)
3. Select region (choose closest to your users)
4. Select tier:
   - **M0 (Free)**: Development/testing only
   - **M2 ($9/month)**: 100 users prototype
   - **M10 ($57/month)**: Production (recommended)
   - **M30+**: High-traffic production

5. Cluster name: `healthcare-cluster`
6. Click "Create Cluster" (takes 3-7 minutes)

### Step 3: Database Security

#### Create Database User

1. Go to "Database Access"
2. Click "Add New Database User"
3. Authentication Method: Password
4. Username: `healthcare_user`
5. Password: Generate secure password (save it!)
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"

#### Configure Network Access

1. Go to "Network Access"
2. Click "Add IP Address"
3. Options:
   - **For testing**: Add your current IP or "Allow Access from Anywhere" (0.0.0.0/0)
   - **For production**: Add your server's static IP address
4. Click "Confirm"

### Step 4: Get Connection String

1. Go to "Database" → Click "Connect"
2. Choose "Connect your application"
3. Driver: Node.js, Version: 5.5 or later
4. Copy connection string:
   ```
   mongodb+srv://healthcare_user:<password>@healthcare-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password
6. Add database name: `healthcare`
   ```
   mongodb+srv://healthcare_user:YOUR_PASSWORD@healthcare-cluster.xxxxx.mongodb.net/healthcare?retryWrites=true&w=majority
   ```

### Step 5: Configure Database

#### Enable Backups (M10+)

1. Go to "Backup" tab
2. Enable "Continuous Backup"
3. Configure retention policy (7-14 days recommended)

#### Configure Alerts

1. Go to "Alerts" tab
2. Enable alerts for:
   - Disk usage > 75%
   - Connections > 80% of max
   - Slow queries
   - Replication lag

---

## Application Deployment

### Option 1: Deploy to VPS (DigitalOcean, Linode, etc.)

#### Step 1: Setup Server

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Verify installation
node --version  # Should be v18.x.x
npm --version
```

#### Step 2: Deploy Application

```bash
# Create application directory
mkdir -p /var/www/healthcare-app
cd /var/www/healthcare-app

# Clone or upload your code
# Option A: Clone from Git
git clone https://github.com/yourusername/healthcare-app.git .

# Option B: Upload via SCP
# On your local machine:
# scp -r healthcare-mongodb-app/* root@your-server-ip:/var/www/healthcare-app/

# Install dependencies
npm install --production

# Build TypeScript
npm run build
```

#### Step 3: Configure Environment

```bash
# Create production .env file
nano .env
```

Add:
```env
MONGODB_URI=mongodb+srv://healthcare_user:YOUR_PASSWORD@healthcare-cluster.xxxxx.mongodb.net/healthcare?retryWrites=true&w=majority
MONGODB_DB_NAME=healthcare
PORT=3000
NODE_ENV=production
API_PREFIX=/api
CORS_ORIGIN=https://yourdomain.com
LOG_LEVEL=info
```

Save and exit (Ctrl+X, Y, Enter)

#### Step 4: Setup Process Manager (PM2)

```bash
# Install PM2 globally
npm install -g pm2

# Start application
pm2 start dist/server.js --name healthcare-app

# Enable startup on boot
pm2 startup
pm2 save

# View logs
pm2 logs healthcare-app

# Monitor
pm2 monit
```

#### Step 5: Setup Nginx Reverse Proxy

```bash
# Install Nginx
apt install -y nginx

# Create Nginx configuration
nano /etc/nginx/sites-available/healthcare-app
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
ln -s /etc/nginx/sites-available/healthcare-app /etc/nginx/sites-enabled/

# Test configuration
nginx -t

# Restart Nginx
systemctl restart nginx
```

#### Step 6: Setup SSL (HTTPS)

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal:
certbot renew --dry-run
```

### Option 2: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create healthcare-app-prod

# Set environment variables
heroku config:set MONGODB_URI="mongodb+srv://..."
heroku config:set NODE_ENV=production

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 3: Deploy to AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI
2. Initialize EB:
   ```bash
   eb init -p node.js healthcare-app
   ```
3. Create environment:
   ```bash
   eb create production-env
   ```
4. Set environment variables in AWS Console
5. Deploy:
   ```bash
   eb deploy
   ```

---

## Environment Configuration

### Production .env File

```env
# MongoDB
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/healthcare?retryWrites=true&w=majority
MONGODB_DB_NAME=healthcare

# Server
PORT=3000
NODE_ENV=production

# API
API_PREFIX=/api
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Security
CORS_ORIGIN=https://yourdomain.com

# Logging
LOG_LEVEL=info
LOG_FILE=logs/app.log

# Data Retention (days)
RAW_SENSOR_TTL=7
PROCESSED_METRICS_TTL=30
DAILY_SUMMARY_TTL=365
PREDICTIONS_TTL=90
```

### Environment Variables Security

Never commit `.env` file to Git!

**Secure storage options:**
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Environment variables in hosting platform

---

## Performance Tuning

### MongoDB Indexes

All critical indexes are created automatically by Mongoose. Verify with:

```javascript
// Run this in MongoDB shell or Compass
db.users.getIndexes()
db.rawSensorData.getIndexes()
db.processedHealthMetrics.getIndexes()
```

### Connection Pool

Already optimized in `src/config/database.ts`:
```typescript
maxPoolSize: 10,
minPoolSize: 2,
```

For high traffic, increase:
```typescript
maxPoolSize: 50,
minPoolSize: 10,
```

### Caching Strategy

Implement Redis caching for:
- User profiles (1 hour TTL)
- Daily summaries (24 hour TTL)
- Latest sensor readings (5 minute TTL)

### Load Testing

```bash
# Install Apache Bench
apt install apache2-utils

# Test API
ab -n 1000 -c 10 http://localhost:3000/health

# Test with POST data
ab -n 100 -c 5 -p sensor-data.json -T application/json http://localhost:3000/api/sensor-data
```

---

## Monitoring

### Application Monitoring

#### PM2 Plus (Recommended)

```bash
# Sign up at https://app.pm2.io
pm2 link YOUR_SECRET_KEY YOUR_PUBLIC_KEY
```

Features:
- Real-time monitoring
- Exception tracking
- Custom metrics
- Alerts

#### Alternative: New Relic

```bash
npm install newrelic
```

Add to `server.ts`:
```typescript
require('newrelic');
```

### Database Monitoring

MongoDB Atlas provides:
- Real-time performance metrics
- Slow query analyzer
- Index suggestions
- Disk usage alerts

Access at: Atlas Console → Cluster → Metrics

### Uptime Monitoring

Free options:
- UptimeRobot (https://uptimerobot.com)
- Pingdom (https://pingdom.com)
- StatusCake (https://statuscake.com)

Configure:
- Check URL: `https://yourdomain.com/health`
- Interval: 5 minutes
- Alert: Email/SMS on failure

### Log Management

#### Centralized Logging with Winston + CloudWatch/Papertrail

```bash
npm install winston-cloudwatch
```

Update `src/utils/logger.ts`:
```typescript
import WinstonCloudWatch from 'winston-cloudwatch';

logger.add(new WinstonCloudWatch({
  logGroupName: 'healthcare-app',
  logStreamName: 'production',
  awsRegion: 'us-east-1',
}));
```

---

## Security

### Checklist

- ✅ Use HTTPS everywhere
- ✅ Environment variables for secrets
- ✅ Rate limiting enabled
- ✅ Helmet.js for HTTP headers
- ✅ Input validation with Joi
- ✅ CORS properly configured
- ✅ MongoDB authentication enabled
- ✅ IP whitelist on MongoDB Atlas
- ✅ Regular security updates
- ✅ No sensitive data in logs

### Additional Security Measures

#### Add Authentication

Install JWT:
```bash
npm install jsonwebtoken bcryptjs
npm install @types/jsonwebtoken @types/bcryptjs --save-dev
```

Create auth middleware:
```typescript
import jwt from 'jsonwebtoken';

export const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ message: 'Unauthorized' });
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Invalid token' });
  }
};
```

#### Enable HIPAA Compliance (if needed)

1. Sign BAA with MongoDB Atlas
2. Enable encryption at rest
3. Enable audit logging
4. Implement access controls
5. Add data anonymization
6. Create incident response plan

---

## Backup & Recovery

### Automated Backups (MongoDB Atlas M10+)

Already enabled in Atlas setup. Features:
- Continuous backup
- Point-in-time recovery
- Cross-region backup
- Automatic retention

### Manual Backups

```bash
# Backup with mongodump
mongodump --uri="mongodb+srv://..." --out=./backup-$(date +%Y%m%d)

# Restore
mongorestore --uri="mongodb+srv://..." ./backup-20251105
```

### Application-Level Backup

Create backup script (`scripts/backup.sh`):
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --uri="$MONGODB_URI" --out=/backups/$DATE
tar -czf /backups/$DATE.tar.gz /backups/$DATE
rm -rf /backups/$DATE
# Upload to S3
aws s3 cp /backups/$DATE.tar.gz s3://your-backup-bucket/
```

Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh
```

---

## Scaling

### Horizontal Scaling

#### Load Balancer Setup

```nginx
upstream healthcare_app {
    least_conn;
    server 10.0.1.10:3000;
    server 10.0.1.11:3000;
    server 10.0.1.12:3000;
}

server {
    listen 80;
    location / {
        proxy_pass http://healthcare_app;
    }
}
```

#### MongoDB Scaling

Atlas Auto-Scaling (M10+):
1. Go to Cluster → Edit Configuration
2. Enable auto-scaling for:
   - Storage (up to 4TB)
   - Compute (up to M80)

### Vertical Scaling

Upgrade MongoDB cluster tier:
- M2 → M10 (for 1,000+ users)
- M10 → M30 (for 10,000+ users)
- M30 → M60 (for 100,000+ users)

### Database Sharding

For massive scale (1M+ users):
1. Enable sharding in Atlas
2. Choose shard key: `userId`
3. Configure zones for geographic distribution

---

## Health Checks

### Kubernetes Deployment

`k8s/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: healthcare-app
  template:
    metadata:
      labels:
        app: healthcare-app
    spec:
      containers:
      - name: healthcare-app
        image: your-registry/healthcare-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: MONGODB_URI
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: uri
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Troubleshooting

### Common Issues

#### Connection Timeout
- Check IP whitelist in MongoDB Atlas
- Verify connection string
- Check firewall rules

#### High Memory Usage
- Increase server RAM
- Optimize queries
- Implement pagination

#### Slow Queries
- Check MongoDB Atlas Performance Advisor
- Add missing indexes
- Optimize aggregation pipelines

### Debug Mode

Enable verbose logging:
```env
LOG_LEVEL=debug
NODE_ENV=development
```

---

## Cost Optimization

### MongoDB Atlas Tiers

| Tier | RAM | Storage | Users | Cost/Month |
|------|-----|---------|-------|------------|
| M0 | 512MB | 512MB | ~50 | Free |
| M2 | 2GB | 2GB | ~100 | $9 |
| M10 | 2GB | 10GB | ~1K | $57 |
| M30 | 8GB | 40GB | ~10K | $240 |

### Optimize Costs

1. **Auto-pause** M0 clusters (free tier)
2. **Reserved capacity** for M10+ (save up to 30%)
3. **Data lifecycle** - TTL indexes auto-delete old data
4. **Compression** - Enabled by default in Atlas
5. **Right-sizing** - Monitor actual usage and downgrade if possible

---

## Checklist: Pre-Launch

- [ ] MongoDB Atlas cluster created and configured
- [ ] Production environment variables set
- [ ] SSL certificate installed
- [ ] Database backups enabled
- [ ] Monitoring and alerts configured
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] API documentation published
- [ ] Error tracking integrated
- [ ] Log management setup
- [ ] Domain configured
- [ ] CORS settings verified
- [ ] Rate limiting tested
- [ ] Health check endpoint working
- [ ] PM2 or process manager configured
- [ ] Database indexes verified
- [ ] Seed data removed (if applicable)

---

## Support & Maintenance

### Regular Tasks

**Daily:**
- Check monitoring dashboards
- Review error logs

**Weekly:**
- Review performance metrics
- Check disk usage
- Verify backups

**Monthly:**
- Security updates
- Dependency updates
- Review and optimize slow queries
- Cost analysis

### Emergency Contacts

- MongoDB Atlas Support: https://support.mongodb.com
- Server Provider Support
- Team contact list

---

**Production deployment complete! 🚀**
