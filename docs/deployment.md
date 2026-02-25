# Deployment Guide

This guide covers deploying the Autonomous AI Operator to AWS using ECS Fargate.

## Prerequisites

- AWS account with appropriate permissions
- Docker installed locally
- GitHub repository
- Environment variables configured

## AWS Infrastructure Setup

### 1. Create RDS PostgreSQL Database

1. Go to AWS Console → RDS → Create database
2. Choose **PostgreSQL**
3. Configuration:
   - Template: Production
   - Engine version: PostgreSQL 15
   - Instance class: db.t3.medium (or larger for production)
   - Storage: 20GB (or larger)
   - Multi-AZ: Yes (for high availability)
4. Connectivity:
   - VPC: Create new VPC
   - Public access: No
   - Security group: Create new
   - Inbound rules: Allow port 5432 from ECS security group
5. Database authentication: Create master username/password
6. Create database: `autonomous_ai_operator`
7. Create database: `autonomous_ai_operator_test` (optional)

### 2. Create ElastiCache Redis

1. Go to AWS Console → ElastiCache → Create cluster
2. Choose **Redis**
3. Configuration:
   - Node type: cache.t3.medium
   - Number of nodes: 1 (or 3 for production)
   - Replication: Yes (for high availability)
4. Security groups: Create new, allow port 6379 from ECS
5. Create cluster: `autonomous-ai-operator`

### 3. Create ECR Repository

1. Go to AWS Console → ECR → Create repository
2. Repository name: `autonomous-ai-operator`
3. Visibility: Public (or Private if needed)
4. Create repository

### 4. Create ECS Cluster

1. Go to AWS Console → ECS → Create cluster
2. Cluster name: `autonomous-ai-operator`
3. Cluster type: EC2 Linux or Fargate
4. Create cluster

### 5. Create ECS Task Definition

1. Go to AWS Console → ECS → Task definitions → Create new task definition
2. Task type: Fargate
3. Task role: Create new role with `AmazonECSTaskExecutionRolePolicy`
4. Network mode: awsvpc
5. Task memory: 2GB (or larger)
6. Task CPU: 1 vCPU (or larger)
7. Container definitions:
   - Name: `autonomous-ai-operator`
   - Image: `your-ecr-repository/autonomous-ai-operator:latest`
   - Memory: 512MB
   - CPU: 256
   - Port mappings: 8000
   - Environment variables:
     - `DATABASE_URL`: `postgresql+asyncpg://user:password@endpoint:5432/autonomous_ai_operator`
     - `REDIS_URL`: `redis://endpoint:6379/0`
     - `APP_ENV`: `production`
     - `DEBUG`: `false`
     - `LOG_LEVEL`: `INFO`
     - `ANTHROPIC_API_KEY`: `your-api-key`
     - `TWILIO_ACCOUNT_SID`: `your-twilio-sid`
     - `VAPI_API_KEY`: `your-vapi-key`
     - `ELEVENLABS_API_KEY`: `your-elevenlabs-key`
     - `SERPER_API_KEY`: `your-serper-key`
   - Secrets (recommended):
     - `ENCRYPTION_KEY`: AWS Secrets Manager
     - `JWT_SECRET`: AWS Secrets Manager
8. Create task definition

### 6. Create ECS Service

1. Go to AWS Console → ECS → Services → Create new service
2. Cluster: `autonomous-ai-operator`
3. Service name: `autonomous-ai-operator-service`
4. Task definition: Select the task definition created above
5. Launch type: Fargate
6. Network configuration:
   - VPC: Select your VPC
   - Subnets: Select public subnets
   - Security groups: Select security group for PostgreSQL and Redis
7. Service type: REPLICA
8. Desired tasks: 2 (for high availability)
9. Auto scaling:
   - Minimum: 1
   - Maximum: 5
   - Target tracking scaling: CPU utilization 70%
10. Create service

### 7. Create Application Load Balancer

1. Go to AWS Console → EC2 → Load Balancers → Create load balancer
2. Load balancer type: Application Load Balancer
3. Name: `autonomous-ai-operator-alb`
4. Scheme: Internet-facing
5. IP address type: IPv4
6. VPC: Select your VPC
7. Security groups: Create new, allow port 80 and 443
8. Listeners:
   - HTTP (80): Redirect to HTTPS
   - HTTPS (443): Forward to ECS target group
9. Target group:
   - Name: `autonomous-ai-operator-tg`
   - Protocol: HTTP
   - Port: 8000
   - VPC: Select your VPC
   - Health check: /health
10. Create load balancer

### 8. Configure DNS

1. Go to AWS Console → Route 53 → Hosted zones
2. Create hosted zone for your domain
3. Create A record pointing to ALB

### 9. Configure Security Groups

**ECS Security Group**:
- Inbound:
  - Port 8000: From ALB security group
  - Port 5432: From RDS security group
  - Port 6379: From Redis security group
- Outbound:
  - All traffic

**RDS Security Group**:
- Inbound:
  - Port 5432: From ECS security group
- Outbound:
  - All traffic

**Redis Security Group**:
- Inbound:
  - Port 6379: From ECS security group
- Outbound:
  - All traffic

## CI/CD Pipeline

The GitHub Actions workflow automatically builds and deploys to AWS.

### 1. Configure GitHub Secrets

Add these secrets to your GitHub repository:

```
AWS_ROLE_ARN=arn:aws:iam::123456789012:role/GitHubActionsRole
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### 2. Create IAM Role for GitHub Actions

1. Go to AWS Console → IAM → Roles → Create role
2. Trusted entity: GitHub Actions
3. Permissions:
   - AmazonEC2ContainerRegistryReadOnly
   - AmazonECSFullAccess
   - AmazonSSMFullAccess
4. Create role
5. Copy the role ARN

### 3. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

The workflow will automatically:
1. Run tests and linting
2. Build Docker image
3. Push to ECR
4. Update ECS task definition
5. Deploy to ECS

## Monitoring & Logging

### CloudWatch Logs

1. Go to AWS Console → CloudWatch → Logs
2. Create log group: `/aws/ecs/autonomous-ai-operator`
3. Configure log retention: 30 days

### CloudWatch Metrics

1. Go to AWS Console → CloudWatch → Metrics
2. Create custom metrics for:
   - Task success rate
   - Average execution time
   - Error rate
   - LLM token usage
   - Call duration

### Alarms

Create CloudWatch alarms for:
- High error rate (>5%)
- High cost (>$50/day)
- Service downtime (>1 minute)
- Memory pressure (>80%)

## Cost Optimization

### Reserved Instances

- RDS: Use Reserved Instances for 1-3 year commitment
- ElastiCache: Use Reserved Nodes for savings

### Spot Instances

- ECS: Use Spot instances for non-critical workloads

### Auto Scaling

- Configure auto scaling to scale down during low traffic
- Set minimum tasks to 1 during off-hours

### Database Optimization

- Use read replicas for read-heavy workloads
- Enable connection pooling
- Use appropriate instance sizes

## Troubleshooting

### Service Not Starting

1. Check CloudWatch logs for errors
2. Verify environment variables
3. Check database connectivity
4. Review ECS task definition

### Database Connection Issues

1. Verify RDS security group allows ECS
2. Check database endpoint and port
3. Verify credentials
4. Test connection from ECS task

### Redis Connection Issues

1. Verify ElastiCache security group allows ECS
2. Check Redis endpoint and port
3. Verify credentials
4. Test connection from ECS task

### High Memory Usage

1. Increase task memory allocation
2. Optimize database queries
3. Implement caching strategies
4. Review application code for memory leaks

## Rollback Procedure

If deployment fails:

1. Go to AWS Console → ECS → Services
2. Select `autonomous-ai-operator-service`
3. Click "Update service"
4. Change task definition to previous version
5. Click "Update"

## Maintenance

### Regular Tasks

- **Daily**: Check CloudWatch alarms
- **Weekly**: Review logs and metrics
- **Monthly**: Review costs and optimize
- **Quarterly**: Update dependencies and security patches

### Backup Strategy

- **Database**: Automated daily backups (RDS)
- **Redis**: No persistence needed for working memory
- **Code**: Git repository with history

## Security Best Practices

1. **Use Secrets Manager** for sensitive data
2. **Enable encryption** at rest and in transit
3. **Regular security scans** with Trivy
4. **Least privilege** IAM roles
5. **Network isolation** with VPC
6. **Regular updates** for dependencies
7. **Audit logging** for all actions

## Performance Tuning

### Database

- Use connection pooling (PgBouncer)
- Implement read replicas
- Optimize queries with indexes
- Use connection pooling

### Redis

- Use Redis Cluster for high availability
- Implement connection pooling
- Use appropriate eviction policies

### Application

- Implement caching strategies
- Use async I/O
- Optimize database queries
- Implement rate limiting

## Scaling Strategy

### Horizontal Scaling

- Auto scale based on CPU utilization
- Auto scale based on request rate
- Scale to 5 tasks minimum, 20 maximum

### Vertical Scaling

- Increase task memory and CPU
- Use larger RDS instance
- Use larger ElastiCache node

## Support

For deployment issues:
1. Check CloudWatch logs
2. Review ECS task logs
3. Check AWS CloudFormation templates
4. Contact support

## Next Steps

After deployment:
1. Test API endpoints
2. Verify database connectivity
3. Test voice and email features
4. Set up monitoring and alerts
5. Configure backup strategy
6. Document custom configurations
