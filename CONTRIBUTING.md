# Contributing to GenAI Bedrock Microservice

Thank you for your interest in contributing to the GenAI Bedrock Microservice project! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.9+
- Terraform >= 1.0
- AWS CLI configured
- Access to Amazon Bedrock Claude 3.5 Haiku model

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/johngiles12345/BedrockMicroservice.git
   cd BedrockMicroservice
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r lambda/requirements.txt
   pip install -r tests/requirements.txt
   ```

3. **Install development tools:**
   ```bash
   pip install flake8 black bandit isort pytest pytest-cov
   ```

## Code Standards

This project follows the Python Development Guidelines and Coding Standards:

### Python Code Standards

- **PEP8 compliance** with 120 character line limits
- **Sphinx docstring conventions** for all functions and classes
- **Type hints** where appropriate
- **Comprehensive error handling** with structured logging

### Code Quality Tools

Run these tools before submitting code:

```bash
# Format code
black lambda/ tests/ --line-length=120
isort lambda/ tests/

# Lint code
flake8 lambda/ tests/ --max-line-length=120

# Security check
bandit -r lambda/

# Run tests
cd tests && python -m pytest test_lambda_function.py -v --cov=../lambda
```

### Terraform Standards

- Use consistent naming conventions
- Include appropriate tags on all resources
- Follow least-privilege security principles
- Document all variables and outputs

## Testing

### Unit Tests

All Lambda function code must have corresponding unit tests:

```bash
cd tests
python -m pytest test_lambda_function.py -v --cov=../lambda --cov-report=html
```

### Integration Tests

Test the deployed API endpoints:

```bash
# Test valid request
curl -X POST https://your-api-id.execute-api.us-west-2.amazonaws.com/prod/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Test prompt"}'

# Test error handling
curl -X POST https://your-api-id.execute-api.us-west-2.amazonaws.com/prod/generate \
  -H 'Content-Type: application/json' \
  -d '{"invalid": "request"}'
```

## Deployment

### Infrastructure Deployment

```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply changes
terraform apply
```

### CI/CD Pipeline

The project includes GitHub Actions workflows for:

- **Terraform CI/CD**: Validates and deploys infrastructure changes
- **Python Tests**: Runs code quality checks and unit tests

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code standards

3. **Run all quality checks:**
   ```bash
   make lint
   make test
   make format
   ```

4. **Commit your changes** with descriptive messages:
   ```bash
   git commit -m "Add feature: description of changes"
   ```

5. **Push to your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Test results and validation

## Code Review Guidelines

### For Contributors

- Ensure all tests pass
- Follow the established code style
- Include appropriate documentation
- Test edge cases and error conditions

### For Reviewers

- Check code quality and standards compliance
- Verify test coverage
- Review security implications
- Validate documentation updates

## Issue Reporting

When reporting issues, please include:

- **Environment details** (Python version, AWS region, etc.)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and logs
- **Screenshots** if applicable

## Security

- Never commit AWS credentials or sensitive data
- Follow least-privilege principles for IAM roles
- Use environment variables for configuration
- Report security vulnerabilities privately

## Documentation

- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Include inline code comments for complex logic
- Update architecture diagrams when needed

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Deploy to production environment

## Getting Help

- Check existing issues and documentation
- Ask questions in pull request discussions
- Contact the development team for complex issues

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in the project documentation and release notes.

Thank you for contributing to the GenAI Bedrock Microservice project!
