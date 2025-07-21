# GenAI Microservice - Bedrock Integration

A serverless application built with Terraform that provides an API Gateway frontend for processing user inputs through AWS Lambda and Amazon Bedrock's Claude 3.5 Haiku model.

## Architecture

- **API Gateway**: REST API endpoint for receiving user inputs
- **Lambda Function**: Python-based function for processing requests and calling Bedrock
- **Amazon Bedrock**: Claude 3.5 Haiku model for AI text generation
- **Region**: us-west-2

## Project Structure

```
.
├── README.md
├── main.tf                 # Main Terraform configuration
├── variables.tf            # Input variables
├── outputs.tf             # Output values
├── terraform.tfvars       # Variable values
├── lambda/
│   ├── requirements.txt   # Python dependencies
│   └── lambda_function.py # Lambda function code
├── docs/                  # Documentation
└── tests/                 # Test files
```

## Requirements

- Terraform >= 1.0
- AWS CLI configured
- Python 3.9+
- Access to Amazon Bedrock Claude 3.5 Haiku model

## Deployment

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Plan the deployment:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

## Usage

After deployment, the API Gateway endpoint will be available for POST requests with JSON payloads containing user input for processing by the Claude 3.5 Haiku model.

## Documentation

Detailed documentation is available in the `docs/` directory.

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## Standards Compliance

This project follows the Python Development Guidelines and Coding Standards as outlined in the project documentation, including:
- PEP8 compliance with 120 character line limits
- Sphinx docstring conventions
- Comprehensive testing with pytest
- Static analysis with flake8, black, and bandit
