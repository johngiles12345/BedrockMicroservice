# Architecture Documentation

## Overview

The GenAI Bedrock Microservice is a serverless application that provides an API Gateway frontend for processing user inputs through AWS Lambda and Amazon Bedrock's Claude 3.5 Haiku model.

## Architecture Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│ API Gateway │───▶│   Lambda    │───▶│   Bedrock   │
│ Application │    │             │    │  Function   │    │ Claude 3.5  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ CloudWatch  │    │ CloudWatch  │
                   │ API Logs    │    │Lambda Logs  │
                   └─────────────┘    └─────────────┘
```

## Components

### API Gateway
- **Type**: REST API
- **Endpoint**: `/generate` (POST)
- **Features**:
  - Request validation
  - CORS support
  - Access logging
  - Integration with Lambda

### Lambda Function
- **Runtime**: Python 3.9
- **Memory**: 256 MB
- **Timeout**: 30 seconds
- **Features**:
  - Input validation
  - Error handling
  - Bedrock integration
  - Structured logging

### Amazon Bedrock
- **Model**: Claude 3.5 Haiku (`anthropic.claude-3-5-haiku-20241022-v1:0`)
- **Region**: us-west-2
- **Features**:
  - High-performance text generation
  - Cost-effective inference
  - Managed service

### CloudWatch
- **Lambda Logs**: Function execution logs
- **API Gateway Logs**: Request/response logs
- **Retention**: 14 days (configurable)

## Security

### IAM Roles and Policies
- Lambda execution role with minimal permissions
- Bedrock invoke permissions scoped to specific model
- CloudWatch logging permissions

### API Security
- Input validation and sanitization
- Request size limits
- Rate limiting (via API Gateway)

## Monitoring and Observability

### Metrics
- Lambda invocation metrics
- API Gateway request metrics
- Bedrock model usage metrics

### Logging
- Structured JSON logging
- Request/response correlation
- Error tracking and alerting

### Alarms
- Lambda error rate
- API Gateway 4xx/5xx errors
- Bedrock throttling

## Scalability

### Auto Scaling
- Lambda: Automatic scaling based on demand
- API Gateway: Handles up to 10,000 requests per second
- Bedrock: Managed scaling

### Performance Optimization
- Lambda warm-up strategies
- Connection pooling
- Response caching (future enhancement)

## Deployment

### Infrastructure as Code
- Terraform for resource provisioning
- Version-controlled configuration
- Environment-specific deployments

### CI/CD Pipeline
- Automated testing
- Security scanning
- Blue-green deployments

## Cost Optimization

### Resource Sizing
- Right-sized Lambda memory allocation
- Optimized CloudWatch log retention
- Pay-per-use Bedrock pricing

### Monitoring
- Cost tracking and alerting
- Usage optimization recommendations
