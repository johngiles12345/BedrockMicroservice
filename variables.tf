variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Name of the project used for resource naming"
  type        = string
  default     = "genai-bedrock-microservice"
}

variable "bedrock_model_id" {
  description = "Bedrock model ID for Claude 3.5 Haiku"
  type        = string
  default     = "anthropic.claude-3-5-haiku-20241022-v1:0"
}

variable "api_stage_name" {
  description = "API Gateway stage name"
  type        = string
  default     = "prod"
}

variable "log_retention_days" {
  description = "CloudWatch log retention period in days"
  type        = number
  default     = 14
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "GenAI-Bedrock-Microservice"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
