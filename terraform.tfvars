# AWS Configuration
aws_region = "us-west-2"

# Project Configuration
project_name = "genai-bedrock-microservice"

# Bedrock Configuration
bedrock_model_id = "anthropic.claude-3-5-haiku-20241022-v1:0"

# API Gateway Configuration
api_stage_name = "prod"

# Logging Configuration
log_retention_days = 14

# Resource Tags
tags = {
  Project     = "GenAI-Bedrock-Microservice"
  Environment = "production"
  ManagedBy   = "terraform"
  Owner       = "development-team"
}
